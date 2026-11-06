"""Gemini TTS (Google AI Studio free tier) narration.

- Key: env GEMINI_API_KEY (repo secret on GitHub; never committed).
- Model: newest model whose name contains "tts", found via the models list (override with GEMINI_TTS_MODEL).
- Free-tier rate limits are tight (~3 requests/min reported), so text is sent in large chunks and calls are spaced.

Usage (samples):  python3 pipeline/voice_gemini.py sample <text_file> <out_dir> [voice ...]
Output: 24 kHz mono 16-bit WAV per voice.
"""
import base64, json, os, re, sys, time, urllib.request, wave

API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "")
# Structured prompt (Google's recommended layout, same as the owner's Six Degrees channel): profile + director's
# notes, then the script under "## TRANSCRIPT". A loose one-line direction got read aloud by several voices; this
# layout marks where the notes end. pipeline/align.py still fails the build if anything off-script is spoken.
STYLE = os.environ.get("GEMINI_TTS_STYLE", """# AUDIO PROFILE: a narrator reading a finished script, word for word.

## DIRECTOR'S NOTES
Style: curious, confident, a little dry and amused; a real lift on each reveal. American accent.
Pace: unhurried and relaxed, about 150 words per minute. A short pause after numbers and before reveals.
Read the transcript below VERBATIM, exactly once, in order. Never add, skip, repeat, summarize or change any words.
Do not read these notes aloud.""")
if STYLE.strip().lower() == "none": STYLE = ""  # some voices (Charon, Iapetus) read any direction aloud
CACHE = os.environ.get("TTS_CACHE", os.path.join(os.path.dirname(__file__), "..", ".tts-cache"))
MIN_GAP = float(os.environ.get("GEMINI_TTS_GAP", "21"))  # seconds between calls (free tier ~3 RPM)
_last = [0.0]

def _req(path, body=None):
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.load(resp)

class DailyQuota(Exception):
    """Free tier allows ~10 requests/day PER MODEL (GenerateRequestsPerDayPerProjectPerModel-FreeTier)."""

def models_ranked():
    """TTS models visible to this key, best first. GEMINI_TTS_MODEL pins one."""
    if os.environ.get("GEMINI_TTS_MODEL"): return [os.environ["GEMINI_TTS_MODEL"]]
    names = [m["name"].split("/", 1)[1] for m in _req("models?pageSize=1000").get("models", []) if "tts" in m["name"].lower()]
    if not names: sys.exit("no TTS model visible to this key")
    def ver(n):
        v = re.findall(r"(\d+(?:\.\d+)?)", n); return float(v[0]) if v else 0
    names.sort(key=lambda n: (ver(n), "flash" in n, "lite" not in n, "preview" not in n), reverse=True)
    print("TTS models (best first):", names, file=sys.stderr)
    return names

def pick_model():
    return models_ranked()[0]

def synth(text, voice, model):
    wait = MIN_GAP - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    prompt = f"{STYLE}\n\n## TRANSCRIPT\n{text}" if STYLE else text
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for attempt in range(5):
        try:
            _last[0] = time.time()
            out = _req(f"models/{model}:generateContent", body)
            part = out["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])  # raw PCM s16le 24 kHz mono
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                err = json.loads(raw)["error"]
                msg = err.get("message", "")
                # Google lists the exact quota hit ("Quota exceeded for metric: ..., limit: ...") and a retry delay
                details = [d for d in err.get("details", []) if d.get("violations") or d.get("retryDelay")]
                msg += " | " + json.dumps(details)[:1500]
            except Exception:
                msg = raw[:1500]
            print(f"  {voice}: HTTP {e.code} {msg}", file=sys.stderr)
            if e.code == 402:
                raise SystemExit("Gemini API: prepaid balance is empty (HTTP 402). Buy credits in AI Studio -> Billing; "
                                 "Google Cloud / Developer Program credits only apply after a Prepay purchase.")
            if e.code == 429 and "PerDay" in raw:
                raise DailyQuota(model)  # waiting won't help until the daily reset; caller tries the next model
            if e.code in (429, 500, 503): time.sleep(30 * (attempt + 1)); continue
            raise
    raise DailyQuota(model)

MAX_WPM = float(os.environ.get("NARRATION_MAX_WPM", "165"))
TARGET_WPM = float(os.environ.get("NARRATION_TARGET_WPM", "155"))

def _atempo(audio, factor):
    """Pitch-preserving tempo change via ffmpeg (factor < 1 = slower). float32 mono 24 kHz in/out."""
    import subprocess, numpy as np
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "f32le", "-ar", "24000", "-ac", "1", "-i", "-",
                        "-af", f"atempo={factor:.4f}", "-f", "f32le", "-ar", "24000", "-ac", "1", "-"],
                       input=audio.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).copy()

def write_wav(pcm, path, sr=24000):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm)

def _chunks(lines, max_words=int(os.environ.get("GEMINI_TTS_CHUNK_WORDS", "250"))):  # long chunks made the model repeat/improvise; ~6 requests per 8-min video
    cur, n = [], 0
    for i, l in enumerate(lines):
        w = len(l.split())
        if cur and n + w > max_words:
            yield cur; cur, n = [], 0
        cur.append(i); n += w
    if cur: yield cur

def say_script(lines, out_wav, gap=0.35, voice=None, synth_fn=None):
    """Same contract as voice.say_script: returns [{text, start, end}] per line and writes out_wav (24 kHz).
    Lines are synthesized in ~600-word chunks (free tier: ~10 requests/day per model), then each line is located
    in its chunk with Whisper word timestamps (pipeline/align.py). Always the best TTS model; if its daily quota
    runs out the build stops (cached chunks are reused on the next run)."""
    if synth_fn:
        return _say(lines, out_wav, gap, voice, synth_fn, None)
    # Best model only (owner's call: every video must sound like the approved Achird sample). No fallback models.
    model = pick_model()
    try:
        print(f"narrating with {model}", file=sys.stderr)
        return _say(lines, out_wav, gap, voice, None, model)
    except DailyQuota:
        raise SystemExit(f"Gemini TTS daily free quota (10 requests/day for {model}) is used up. It resets at midnight "
                         "Pacific; voiced chunks are cached, so the next run only voices what's missing.")

def _say(lines, out_wav, gap, voice, synth_fn, model):
    import numpy as np
    from align import transcribe_words, line_times, inserted_speech, novel_words
    voice = voice or os.environ.get("GEMINI_TTS_VOICE", "Achird")  # owner's pick (with the structured prompt)
    clean = [re.sub(r"\s*\[pause(?: [\d.]+)?\]\s*", "... ", l).strip() for l in lines]
    synth_fn = synth_fn or (lambda text: np.frombuffer(synth(text, voice, model), np.int16).astype(np.float32) / 32768)
    parts, timing, t0 = [], [], 0.0
    for idx in _chunks(clean):
        chunk_lines = [clean[i] for i in idx]
        text = "\n".join(chunk_lines)
        import hashlib
        key = hashlib.sha256(f"{voice}|{STYLE}|{model}|{text}".encode()).hexdigest()[:20]
        cpath = os.path.join(CACHE, f"{key}.npy")
        if os.path.exists(cpath):
            audio = np.load(cpath)
        else:
            audio = synth_fn(text)          # float32 @ 24 kHz
            os.makedirs(CACHE, exist_ok=True); np.save(cpath, audio)
        # Pace QA: words here are spelled out ("fifty-one thousand..."), so ~150-160 wpm sounds natural.
        # If the model still rushes, slow the chunk with pitch-preserving time-stretch (at most 12%).
        wpm = len(text.split()) / (len(audio) / 24000 / 60)
        if wpm > MAX_WPM:
            factor = max(0.88, TARGET_WPM / wpm)
            audio = _atempo(audio, factor)
            print(f"  pace {wpm:.0f} wpm > {MAX_WPM:.0f}: slowed x{factor:.2f} -> {wpm * factor:.0f} wpm", file=sys.stderr)
        else:
            print(f"  pace {wpm:.0f} wpm (ok)", file=sys.stderr)
        dur = len(audio) / 24000
        a16 = np.interp(np.arange(0, len(audio), 1.5), np.arange(len(audio)), audio).astype(np.float32)
        heard = transcribe_words(a16)
        spans, anchored = line_times(chunk_lines, heard, dur)
        ins = inserted_speech(chunk_lines, heard)
        if ins:
            novel = novel_words(chunk_lines, ins)
            spoken_wpm = len(text.split()) / (dur / 60)
            if len(novel) >= 3:  # words that are nowhere in the script: improvised / directions read aloud
                os.remove(cpath) if os.path.exists(cpath) else None
                raise SystemExit(f"narration contains words that aren't in the script ({novel[:12]}): \"{ins[:300]}\". Chunk discarded; re-run.")
            if spoken_wpm < 0.85 * TARGET_WPM:  # script words repeated AND the audio really is too long
                os.remove(cpath) if os.path.exists(cpath) else None
                raise SystemExit(f"narration repeats part of the script (pace {spoken_wpm:.0f} wpm): \"{ins[:300]}\". Chunk discarded; re-run.")
            print(f"  note: transcript shows a repeat but pace is normal ({spoken_wpm:.0f} wpm): treating as a transcription glitch", file=sys.stderr)
        print(f"  chunk {len(timing) // 1}: {len(idx)} lines, {dur:.1f}s, anchored {anchored}/{len(idx)}", file=sys.stderr)
        if anchored < 0.7 * len(idx):  # long chunks can get cut off; never ship a video with missing narration
            os.remove(cpath) if os.path.exists(cpath) else None
            raise SystemExit(f"narration chunk looks incomplete ({anchored}/{len(idx)} lines heard). "
                             "Lower GEMINI_TTS_CHUNK_WORDS and re-run.")
        for i, (s0, s1) in zip(idx, spans):
            timing.append({"text": re.sub(r"\[pause[^\]]*\]", "", lines[i]).strip(), "start": round(t0 + s0, 3), "end": round(t0 + s1, 3)})
        parts += [audio, np.zeros(int(24000 * gap), np.float32)]
        t0 += dur + gap
    import soundfile as sf
    sf.write(out_wav, np.concatenate(parts), 24000)
    return timing

if __name__ == "__main__":
    if not KEY: sys.exit("GEMINI_API_KEY is not set")
    cmd, text_file, out = sys.argv[1], sys.argv[2], sys.argv[3]
    voices = sys.argv[4:] or ["Charon", "Iapetus", "Puck", "Orus", "Sadaltager", "Achird"]
    os.makedirs(out, exist_ok=True)
    text = open(text_file, encoding="utf-8").read().strip()
    model = pick_model(); print("model:", model)
    for v in voices:
        pcm = synth(text, v, model)
        write_wav(pcm, os.path.join(out, f"gemini_{v}.wav"))
        print(f"{v}: {len(pcm) / 48000:.1f}s")
