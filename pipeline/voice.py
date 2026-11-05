"""Narration TTS: Kokoro-82M (local ONNX), voice = 70% am_michael + 30% am_onyx, speed 1.25.
Matches the channel voice chosen by the creator. No EQ/compression on the voice; loudness-normalise the final mix only.

say_script(lines, out_wav) -> list of {text, start, end} per line, used to time scenes.
Lines may contain [pause] / [pause 0.8] marks (inserted silence)."""
import re, json, sys, os
import numpy as np, soundfile as sf

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
SR = 24000
_k = None
# Respellings for words Kokoro mispronounces (extend as found).
RESPELL = {
    "Steam": "Steam", "roguelite": "rogue-light", "roguelike": "rogue-like", "Elden": "Elden",
    "FromSoft": "From Soft", "FromSoftware": "From Software", "Baldur's": "Balder's", "indie": "indie",
    "%": " percent", "vs.": "versus", "vs": "versus",
}

def _kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
    return _k

def _style():
    k = _kokoro()
    return k.get_voice_style("am_michael") * 0.7 + k.get_voice_style("am_onyx") * 0.3

def _prep(text):
    for a, b in RESPELL.items():
        text = text.replace(a, b) if not a.isalpha() else re.sub(rf"\b{re.escape(a)}\b", b, text)
    return text

def say_script(lines, out_wav, gap=0.28):
    k, style = _kokoro(), _style()
    chunks, timing, t = [], [], 0.0
    for line in lines:
        parts = re.split(r"(\[pause(?: [\d.]+)?\])", line)
        start = t
        for p in parts:
            m = re.fullmatch(r"\[pause(?: ([\d.]+))?\]", p.strip()) if p.strip() else None
            if m:
                d = float(m.group(1) or 0.7); chunks.append(np.zeros(int(SR * d), np.float32)); t += d
            elif p.strip():
                audio, sr = k.create(_prep(p.strip()), voice=style, speed=1.25, lang="en-us")
                chunks.append(audio.astype(np.float32)); t += len(audio) / sr
        timing.append({"text": re.sub(r"\[pause[^\]]*\]", "", line).strip(), "start": round(start, 3), "end": round(t, 3)})
        chunks.append(np.zeros(int(SR * gap), np.float32)); t += gap
    sf.write(out_wav, np.concatenate(chunks), SR)
    return timing

if __name__ == "__main__":
    lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
    tm = say_script(lines, sys.argv[2])
    json.dump(tm, open(sys.argv[2].rsplit(".", 1)[0] + ".timing.json", "w"), indent=1)
    words = sum(len(x["text"].split()) for x in tm)
    print(f"{len(tm)} lines, {tm[-1]['end']:.1f}s, {words} words, {words / (tm[-1]['end'] / 60):.0f} wpm")
