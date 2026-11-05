"""Flag narration that reads as AI-written before it goes to the voice model.

Usage: python3 pipeline/script_lint.py script.md [--strict]

Rules are drawn from Wikipedia's "Signs of AI writing" field guide (WikiProject AI Cleanup,
Oct 2026 revision) plus YouTube-narration clichés. Most rules are warnings, not proof:
the goal is a script that sounds like a specific person who did the work.
Exit code 1 if the script fails (score above threshold or any hard ban hit).
"""
import re, sys, statistics

# --- hard bans: never in narration ---------------------------------------
HARD = {
    "ai vocabulary": r"\b(delve|tapestry|testament|underscor\w*|pivotal|intricac\w*|intricate|meticulous\w*|"
                     r"vibrant|bolster\w*|garner\w*|showcas\w*|fostering|foster|interplay|multifaceted|"
                     r"boasts?|enduring|ever-evolving|evolving landscape|landscape of|realm|embark|"
                     r"navigat(e|ing) the|game[- ]changer|unlock(ing)? the|leverage|seamless\w*|"
                     r"in today's|nestled|groundbreaking|renowned|indelible|deeply rooted)\b",
    "significance puffery": r"\b(stands? as|serves? as|is a testament|a crucial role|a pivotal (role|moment)|"
                            r"reflects broader|setting the stage|marking a shift|key turning point|focal point|"
                            r"plays? a (key|vital|crucial|significant) role)\b",
    "chatbot residue": r"\b(it'?s (important|worth) (to note|noting)|it is important to note|in conclusion|"
                       r"in summary|overall,|ultimately,|let me know|i hope this helps|certainly!|great question)\b",
    "youtube clichés": r"\b(let'?s (dive|jump|get) (in|into|right)|buckle up|without further ado|"
                       r"stick around (until|till) the end|smash (that|the) like|in this video,? (we|i)('ll| will)|"
                       r"but here'?s the (thing|kicker|catch)|here'?s where it gets interesting|"
                       r"the answer (may|might|will) surprise you|you won'?t believe|"
                       r"spoiler alert|plot twist|fast forward to|little did (they|we|he|she) know)\b",
    "hedging": r"\b(based on (the )?available (information|data)|not widely (documented|available)|"
               r"does not (by itself )?establish|should be (treated|viewed|seen) as .{0,40} rather than)\b",
}
# --- soft signals: counted per 1,000 words -------------------------------
SOFT = {
    "negative parallelism (not X, it's Y / not just…but)": r"\b(it'?s not (just |only )?[^.?!]{1,40}[,;—-]+ it'?s|not (just|only) [^.?!]{1,40} but( also)?|isn'?t (just )?about [^.?!]{1,40}[,;—-]+ it'?s about)",
    "'rather than' contrast": r"\brather than\b",
    "dangling -ing analysis (', highlighting…')": r",\s+(highlighting|underscoring|emphasizing|reflecting|symbolizing|ensuring|contributing|showcasing|cementing|solidifying)\b",
    "vague attribution": r"\b(experts (say|argue|agree)|many (believe|fans say|people think)|observers|critics argue|some say|studies show)\b",
    "em/en dash": r"[—–]",
    "rhetorical 'So what…?' / 'But why?'": r"(^|\s)(so|but) (what|why|how)\b[^.?!]{0,40}\?",
    "intensifier filler": r"\b(truly|incredibly|absolutely|literally|genuinely|remarkably|undeniably|quietly)\b",
}
SOFT_LIMIT = {  # max per 1,000 words before it counts against the script
    "negative parallelism (not X, it's Y / not just…but)": 1.0,
    "'rather than' contrast": 1.0,
    "dangling -ing analysis (', highlighting…')": 0.5,
    "vague attribution": 0.5,
    "em/en dash": 2.0,
    "rhetorical 'So what…?' / 'But why?'": 2.0,
    "intensifier filler": 2.0,
}

def sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if len(s.split()) >= 1]

def lint(text):
    # strip markdown headings / stage directions in [brackets] — they are not spoken
    spoken = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
    spoken = re.sub(r"\[[^\]]*\]", " ", spoken)
    words = re.findall(r"[A-Za-z0-9'’,.%$-]+", spoken)
    n = max(len(words), 1)
    issues, hard_hits, penalty = [], 0, 0.0
    low = spoken.lower()

    for name, pat in HARD.items():
        hits = [m.group(0) for m in re.finditer(pat, low)]
        if hits:
            hard_hits += len(hits)
            issues.append(f"HARD  {name}: {len(hits)} → {sorted(set(hits))[:8]}")

    for name, pat in SOFT.items():
        c = len(re.findall(pat, low, re.M))
        rate = c * 1000 / n
        if rate > SOFT_LIMIT[name]:
            penalty += rate - SOFT_LIMIT[name]
            issues.append(f"soft  {name}: {c} ({rate:.1f}/1k words, limit {SOFT_LIMIT[name]})")

    # rule of three: "X, Y, and Z" lists
    triads = len(re.findall(r"\b[\w'-]+(?: [\w'-]+){0,3}, [\w'-]+(?: [\w'-]+){0,3},? and [\w'-]+", low))
    if triads * 1000 / n > 3:
        penalty += triads * 1000 / n - 3
        issues.append(f"soft  rule-of-three lists: {triads} ({triads*1000/n:.1f}/1k words, limit 3)")

    # rhythm: AI narration clusters at 8-20 words with low variance ("burstiness")
    sl = [len(s.split()) for s in sentences(spoken)]
    if len(sl) >= 8:
        mid = sum(1 for x in sl if 8 <= x <= 20) / len(sl)
        cv = statistics.pstdev(sl) / statistics.mean(sl)
        short = sum(1 for x in sl if x <= 5) / len(sl)
        longest = max(sl)
        if mid > 0.70:
            penalty += (mid - 0.70) * 20
            issues.append(f"soft  monotone rhythm: {mid:.0%} of sentences are 8-20 words (want ≤70%)")
        if cv < 0.45:
            penalty += (0.45 - cv) * 20
            issues.append(f"soft  low sentence-length variation (CV {cv:.2f}, want ≥0.45)")
        if short < 0.12:
            issues.append(f"soft  few punchy lines: {short:.0%} of sentences ≤5 words (want ≥12%)")
            penalty += 1
        if longest > 40:
            issues.append(f"soft  a {longest}-word sentence is too long to speak in one breath")
            penalty += 1
    # specificity: concrete numbers & proper nouns per 100 words (data channel = specifics)
    nums = len(re.findall(r"\b\d[\d,.]*%?", spoken))
    propers = len(re.findall(r"(?<![.?!]\s)(?<!^)\b[A-Z][a-z]+", spoken))
    spec = (nums + propers) * 100 / n
    if spec < 4:
        penalty += (4 - spec)
        issues.append(f"soft  low specificity: {spec:.1f} numbers/names per 100 words (want ≥4)")
    # questions: some are good, wall-to-wall is a tell
    q = spoken.count("?") / max(len(sl), 1)
    if q > 0.15:
        penalty += (q - 0.15) * 20
        issues.append(f"soft  too many questions: {q:.0%} of sentences")

    # narrator presence: top-video transcripts use "you" ~20/1k and "I/my/me" ~37/1k words;
    # flops ~6 and ~4. A narrator who is a person, talking to a person.
    you = len(re.findall(r"\b(you|you're|your|you've|you'd)\b", low)) * 1000 / n
    me = len(re.findall(r"\b(i|i'm|i've|i'd|my|me)\b", low)) * 1000 / n
    if you < 10:
        penalty += (10 - you) / 4
        issues.append(f"soft  little direct address: 'you' {you:.0f}/1k words (hits median ~20)")
    if me < 15:
        penalty += (15 - me) / 5
        issues.append(f"soft  narrator absent: 'I/my/me' {me:.0f}/1k words (hits median ~37)")

    wpm_minutes = n / 175   # measured median of top videos: 174 wpm
    return dict(words=n, minutes_at_175wpm=round(wpm_minutes, 1), hard=hard_hits,
                penalty=round(penalty, 1), issues=issues,
                passed=hard_hits == 0 and penalty <= 5)

if __name__ == "__main__":
    r = lint(open(sys.argv[1], encoding="utf-8").read())
    print(f"{r['words']} words ≈ {r['minutes_at_175wpm']} min at 175 wpm | hard hits {r['hard']} | soft penalty {r['penalty']}")
    for i in r["issues"]:
        print("  " + i)
    print("PASS" if r["passed"] else "FAIL")
    sys.exit(0 if r["passed"] else 1)
