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
# Short "Read aloud ...:" lead-in, like Google's own examples. A long paragraph of direction sometimes gets
# read out as part of the script (Charon and Iapetus did this in the first audition).
STYLE = os.environ.get("GEMINI_TTS_STYLE",
    "Read aloud in a relaxed, conversational YouTube-narrator voice, dry and curious, never like a news anchor:")
MIN_GAP = float(os.environ.get("GEMINI_TTS_GAP", "21"))  # seconds between calls (free tier ~3 RPM)
_last = [0.0]

def _req(path, body=None):
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.load(resp)

def pick_model():
    if os.environ.get("GEMINI_TTS_MODEL"): return os.environ["GEMINI_TTS_MODEL"]
    names = [m["name"].split("/", 1)[1] for m in _req("models?pageSize=1000").get("models", []) if "tts" in m["name"].lower()]
    if not names: sys.exit("no TTS model visible to this key")
    def ver(n):
        v = re.findall(r"(\d+(?:\.\d+)?)", n); return float(v[0]) if v else 0
    names.sort(key=lambda n: (ver(n), "flash" in n, "lite" not in n, "preview" not in n))
    print("TTS models visible:", names, file=sys.stderr)
    return names[-1]

def synth(text, voice, model):
    wait = MIN_GAP - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    body = {"contents": [{"parts": [{"text": f"{STYLE}\n\n{text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for attempt in range(5):
        try:
            _last[0] = time.time()
            out = _req(f"models/{model}:generateContent", body)
            part = out["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])  # raw PCM s16le 24 kHz mono
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            print(f"  {voice}: HTTP {e.code} {msg}", file=sys.stderr)
            if e.code in (429, 500, 503): time.sleep(30 * (attempt + 1)); continue
            raise

def write_wav(pcm, path, sr=24000):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm)

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
