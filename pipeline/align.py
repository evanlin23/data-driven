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
    segs, _ = _model[0].transcribe(pcm_f32_16k, beam_size=1, word_timestamps=True, condition_on_previous_text=False,
                                   vad_filter=True)  # avoids Whisper repetition loops
    out = []
    for s in segs:
        for w in s.words or []:
            for t in _tok(w.word):
                out.append((t, w.start, w.end))
    return out

def line_times(lines, words, chunk_dur):
    """lines: script lines in this chunk. words: [(token, start, end)]. Returns [(start, end)] per line (seconds), anchored.
    Also sets line_times.cover = [(matched, total) anchor tokens per line] and line_times.tail_ok (2 of the last 4 anchors heard),
    read by the narration guard straight after the call."""
    sc = []  # (token, line_index) for anchor-able script tokens
    for li, l in enumerate(lines):
        for t in _tok(l):
            if _keep_script(t): sc.append((t, li))
    hw = [(t, s, e) for t, s, e in words if _keep_heard(t)]
    sm = difflib.SequenceMatcher(a=[t for t, _ in sc], b=[t for t, _, _ in hw], autojunk=False)
    first = [None] * len(lines); last = [None] * len(lines)
    hit = [0] * len(lines); matched_sc = set()
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            li = sc[a + k][1]; s, e = hw[b + k][1], hw[b + k][2]
            hit[li] += 1; matched_sc.add(a + k)
            if first[li] is None or s < first[li]: first[li] = s
            if last[li] is None or e > last[li]: last[li] = e
    # A line starts at its first anchor, but leading numbers / "and" / "a" aren't anchors ("Ninety-six percent...").
    # Pull the start back to the first heard word (of any kind) after the previous line's last matched word.
    prev_end = 0.0
    for i in range(len(lines)):
        if first[i] is not None:
            earlier = [s for t, s, e in words if prev_end - 0.05 <= s < first[i]]
            if earlier: first[i] = min(earlier)
        if last[i] is not None: prev_end = last[i]
    # fill gaps by interpolation on cumulative character share
    lens = np.cumsum([0] + [len(l) for l in lines]); tot = lens[-1] or 1
    est = [chunk_dur * lens[i] / tot for i in range(len(lines))]
    starts = [first[i] if first[i] is not None else est[i] for i in range(len(lines))]
    starts[0] = 0.0
    for i in range(1, len(starts)):  # keep monotonic
        starts[i] = max(starts[i], starts[i - 1] + 0.3)
    ends = [starts[i + 1] for i in range(len(lines) - 1)] + [chunk_dur]
    anchored = sum(f is not None for f in first)
    line_times.flags = [f is not None for f in first]
    totals = [sum(1 for _, li in sc if li == i) for i in range(len(lines))]
    line_times.cover = list(zip(hit, totals))
    line_times.tail_ok = sum(j in matched_sc for j in range(max(0, len(sc) - 4), len(sc))) >= min(2, len(sc))  # 2 of the last 4 anchors
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


def repeat_seconds(lines, words, min_run=6):
    """Seconds of audio taken by the longest run of heard words that the script doesn't account for, counting only time
    that doesn't overlap words matched to the script. A real spoken repeat takes real time (several seconds); a Whisper
    transcription loop usually re-emits text over audio that is already matched, so it adds ~0 s."""
    sc = [t for l in lines for t in _tok(l) if _keep_script(t)]
    hw = [(t, s, e) for t, s, e in words if _keep_heard(t)]
    sm = difflib.SequenceMatcher(a=sc, b=[t for t, _, _ in hw], autojunk=False)
    blocks = sm.get_matching_blocks()
    matched = [(hw[b + k][1], hw[b + k][2]) for a, b, n in blocks for k in range(n)]
    worst, pa, pb = [], 0, 0
    for a, b, n in blocks:
        gap = hw[pb:b]
        if len(gap) >= min_run and (a - pa) < len(gap) // 2 and len(gap) > len(worst): worst = gap
        pa, pb = a + n, b + n
    if not worst: return 0.0
    lo, hi = worst[0][1], worst[-1][2]
    overlap = sum(max(0.0, min(hi, e) - max(lo, s)) for s, e in matched)
    return max(0.0, (hi - lo) - overlap)
