"""Find when each script line is spoken in a narration chunk (for engines that synthesize many lines at once).

Uses faster-whisper word timestamps, then aligns script words to transcript words with difflib.
Numbers are ignored on both sides (script says "ninety-six percent", Whisper writes "96%"); the remaining
words anchor each line. Lines with no anchor are interpolated between their neighbours.
"""
import difflib, re
import numpy as np

NUMWORDS = set("""zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen
seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion
percent point and a""".split())
_model = [None]

def _tok(s):
    return [w for w in re.findall(r"[a-z']+|\d[\d,.%$]*", s.lower().replace("-", " ")) if w]

def _keep_script(w): return w not in NUMWORDS and not w[0].isdigit()
def _keep_heard(w): return not any(c.isdigit() for c in w) and w not in NUMWORDS

def transcribe_words(pcm_f32_16k):
    if _model[0] is None:
        from faster_whisper import WhisperModel
        _model[0] = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = _model[0].transcribe(pcm_f32_16k, beam_size=1, word_timestamps=True, condition_on_previous_text=False)  # avoids Whisper repetition loops
    out = []
    for s in segs:
        for w in s.words or []:
            for t in _tok(w.word):
                out.append((t, w.start, w.end))
    return out

def line_times(lines, words, chunk_dur):
    """lines: script lines in this chunk. words: [(token, start, end)]. Returns [(start, end)] per line (seconds)."""
    sc = []  # (token, line_index) for anchor-able script tokens
    for li, l in enumerate(lines):
        for t in _tok(l):
            if _keep_script(t): sc.append((t, li))
    hw = [(t, s, e) for t, s, e in words if _keep_heard(t)]
    sm = difflib.SequenceMatcher(a=[t for t, _ in sc], b=[t for t, _, _ in hw], autojunk=False)
    first = [None] * len(lines); last = [None] * len(lines)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            li = sc[a + k][1]; s, e = hw[b + k][1], hw[b + k][2]
            if first[li] is None or s < first[li]: first[li] = s
            if last[li] is None or e > last[li]: last[li] = e
    # fill gaps by interpolation on cumulative character share
    lens = np.cumsum([0] + [len(l) for l in lines]); tot = lens[-1] or 1
    est = [chunk_dur * lens[i] / tot for i in range(len(lines))]
    starts = [first[i] if first[i] is not None else est[i] for i in range(len(lines))]
    starts[0] = 0.0
    for i in range(1, len(starts)):  # keep monotonic
        starts[i] = max(starts[i], starts[i - 1] + 0.3)
    ends = [starts[i + 1] for i in range(len(lines) - 1)] + [chunk_dur]
    anchored = sum(f is not None for f in first)
    return list(zip(starts, ends)), anchored


def inserted_speech(lines, words, min_run=6):
    """Return text of the longest run (>= min_run words) heard in the audio that has no counterpart in the script,
    e.g. a TTS model reading its delivery direction aloud. ASR slips rarely produce 6+ consecutive unmatched words."""
    sc = [t for l in lines for t in _tok(l) if _keep_script(t)]
    hw = [t for t, _, _ in words if _keep_heard(t)]
    sm = difflib.SequenceMatcher(a=sc, b=hw, autojunk=False)
    worst, pa, pb = [], 0, 0
    for a, b, n in sm.get_matching_blocks():
        gap_heard, gap_script = hw[pb:b], sc[pa:a]
        if len(gap_heard) >= min_run and len(gap_script) < len(gap_heard) // 2 and len(gap_heard) > len(worst):
            worst = gap_heard
        pa, pb = a + n, b + n
    return " ".join(worst)


def novel_words(lines, text):
    """Words in `text` that appear nowhere in the script lines (improvised content), ignoring numbers."""
    vocab = {t for l in lines for t in _tok(l)}
    return [w for w in text.split() if w not in vocab and _keep_heard(w)]
