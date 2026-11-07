"""Kit self-tests: every gate must fire on a known-bad input and pass a clean one (pattern from the Buh Simulates
kit's test_qa_gates). Run: python3 pipeline/kit/test_kit.py   (needs ffmpeg + numpy; ~30 s)"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kit.audio import decoded_peak_dbfs, lufs, mux  # noqa: E402
from kit.gates import pixel_gate  # noqa: E402

T = tempfile.mkdtemp()
ff = lambda *a: subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *a], check=True)
ok = True
def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}")

# a moving test picture (never blank, no flashes)
clean = f"{T}/clean.mp4"
ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=6", "-pix_fmt", "yuv420p", clean)
check("pixel gate passes a clean clip", pixel_gate(clean) == [])
bad = f"{T}/bad.mp4"
ff("-i", clean, "-vf", "drawbox=c=white:t=fill:enable='eq(n,60)',drawbox=c=black:t=fill:enable='between(n,120,135)'", "-pix_fmt", "yuv420p", bad)
f = pixel_gate(bad)
check("pixel gate catches a 1-frame flash", any("flash" in x for x in f))
check("pixel gate catches a blank run", any("blank" in x for x in f))

# mux: hot (peaky, 24 kHz) and quiet voices both land at -14 LUFS +-0.4 with decoded peak <= -1 dBFS
for name, gain in (("hot", 12), ("quiet", -18)):
    wav = f"{T}/{name}.wav"
    ff("-f", "lavfi", "-i", "sine=f=220:d=6,aformat=sample_rates=24000", "-f", "lavfi", "-i", "anoisesrc=d=6:a=0.3:r=24000",
       "-filter_complex", f"[0][1]amix=inputs=2,volume={gain}dB,apulsator=hz=3", wav)
    out = f"{T}/{name}.mp4"
    m = mux(clean, wav, out)
    check(f"mux {name}: {m['lufs']:.1f} LUFS, decoded peak {m['peak_dbfs']:.2f} dBFS",
          abs(lufs(out) + 14) <= 1.0 and decoded_peak_dbfs(out) <= -1.0)
print("ALL PASS" if ok else "FAILURES")
sys.exit(0 if ok else 1)
