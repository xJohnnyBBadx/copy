#!/usr/bin/env python3
"""COPY tells linter.

Deterministic evidence for the `audit`, `humanize`, `critique` and `polish`
commands. It finds candidate template and machine-made patterns and reports
rhythm metrics. Its output is evidence, not a verdict: every hit must be
confirmed against reference/tells.md before it is reported to a user.

Standard library only. Python 3.8+.

Usage:
  python3 tells.py [--json] [--context N] [--avoid "a,b"] [--allow "c,d"] FILE|-
Exit codes: 0 no findings, 2 findings, 1 error.
"""

import argparse
import json
import re
import statistics
import sys

# --------------------------------------------------------------------------
# Phrase families. Each entry: (regex, note). Matched case-insensitively.
# Family IDs match the headings in reference/tells.md.
# --------------------------------------------------------------------------

FAMILIES = {
    "residue": [
        (r"\bcertainly!", "chatbot opener"),
        (r"\bgreat question\b", "chatbot opener"),
        (r"\bi hope this helps\b", "chatbot sign-off"),
        (r"\bas an ai\b|\bas a language model\b", "model self-reference"),
        (r"\bhere(?:'s| is) (?:a|the|your) (?:revised|rewritten|updated|improved|polished) version\b", "chatbot framing"),
        (r"\[(?:your|insert|company|product|brand|name|customer|statistic|number)\b[^\]\n]{0,40}\]", "unfilled placeholder"),
        (r"\bknowledge cut-?off\b", "model self-reference"),
        (r"\bfeel free to (?:adjust|modify|customi[sz]e|tweak)\b", "chatbot sign-off"),
        (r"\blet me know if you(?:'d| would)? like\b", "chatbot sign-off"),
    ],
    "vocab": [
        (r"\bdelv(?:e|es|ed|ing)\b", "stock vocabulary"),
        (r"\btapestr(?:y|ies)\b", "stock vocabulary"),
        (r"\btestament to\b", "stock vocabulary"),
        (r"\brealm of\b", "stock vocabulary"),
        (r"\bever-evolving\b", "stock vocabulary"),
        (r"\bfast-paced (?:world|environment|landscape|market|age)\b", "stock vocabulary"),
        (r"\bgame[- ]chang(?:er|ers|ing)\b", "stock vocabulary"),
        (r"\bsynerg(?:y|ies|istic)\b", "stock vocabulary"),
        (r"\bleverag(?:e|es|ed|ing)\b", "stock vocabulary (fine in finance: debt leverage)"),
        (r"\bunlock(?:s|ed|ing)? (?:the |your |their |its |our |new )?(?:full |true |hidden )?(?:potential|value|power|possibilities|growth|insights?)\b", "stock vocabulary"),
        (r"\belevat(?:e|es|ed|ing) (?:your|the|their|our|every)\b", "stock vocabulary"),
        (r"\bempower(?:s|ed|ing|ment)?\b", "stock vocabulary"),
        (r"\bseamless(?:ly)?\b", "stock vocabulary"),
        (r"\bcutting[- ]edge\b", "stock vocabulary"),
        (r"\bholistic(?:ally)?\b", "stock vocabulary"),
        (r"\bpivotal\b", "stock vocabulary"),
        (r"\bembark(?:s|ed|ing)? on\b", "stock vocabulary"),
        (r"\byour [\w-]+ journey\b", "stock vocabulary"),
        (r"\bharness(?:es|ed|ing)? the (?:power|potential)\b", "stock vocabulary"),
        (r"\bfoster(?:s|ed|ing)?\b", "stock vocabulary"),
        (r"\bstreamlin(?:e|es|ed|ing)\b", "stock vocabulary"),
        (r"\brevolutioni[sz](?:e|es|ed|ing)\b", "stock vocabulary"),
        (r"\btransformative\b", "stock vocabulary"),
        (r"\bparadigm(?:s| shift)?\b", "stock vocabulary"),
        (r"\bthe [\w-]+ landscape\b", "stock vocabulary (literal for scenery)"),
        (r"\bnavigat(?:e|es|ing) the (?:complexit\w*|challenges|landscape|world|waters)\b", "stock vocabulary"),
        (r"\bin today's [\w-]+ (?:world|landscape|environment|age|market|economy)\b", "stock vocabulary"),
        (r"\brobust\b", "stock vocabulary (literal in engineering and statistics)"),
        (r"\bvibrant\b", "stock vocabulary"),
        (r"\bmeticulous(?:ly)?\b", "stock vocabulary"),
        (r"\bsupercharg(?:e|es|ed|ing)\b", "stock vocabulary"),
        (r"\bnext level\b", "stock vocabulary"),
    ],
    "throat": [
        (r"\bhere's (?:the thing|what|why|how)\b", "throat-clearing"),
        (r"\bit(?:'s| is) worth (?:noting|mentioning)\b", "throat-clearing"),
        (r"\blet(?:'s| us) dive in(?:to)?\b|\bdive (?:deep|right) in(?:to)?\b|\bdeep dive\b", "throat-clearing"),
        (r"\bin this (?:article|post|guide|blog post|piece),? (?:we'll|we will|you'll|you will|i'll|i will)\b", "signposting"),
        (r"\bat the end of the day\b", "throat-clearing"),
        (r"\bwhen it comes to\b", "throat-clearing"),
        (r"\bthe (?:truth|reality) is\b", "throat-clearing"),
        (r"\blet me be clear\b", "throat-clearing"),
        (r"\bit goes without saying\b|\bneedless to say\b", "throat-clearing"),
        (r"\bwithout further ado\b", "throat-clearing"),
        (r"\bmake no mistake\b|\blet that sink in\b", "emphasis crutch"),
    ],
    "reveal": [
        (r"\b(?:it|this|that)(?:'s| is| was)\s+not\s+(?:just\s+|only\s+|merely\s+|about\s+)?[^.!?\n]{1,80}?[,;:—–]\s*(?:it|this|that)(?:'s| is| was)\b", "reveal construction"),
        (r"\b(?:isn't|aren't|wasn't|is not|are not)\s+(?:just\s+|only\s+|merely\s+)?(?:a\s+|an\s+|the\s+|about\s+)?[^.!?\n]{1,60}?[.;:—–]\s*(?:it|this|that|they|we)(?:'s|'re| is| are)\b", "reveal construction"),
        (r"\bnot (?:just|only|merely) (?:a |an |the |about )?[^.!?\n]{1,60}?,?\s+but(?: also)?\b", "reveal construction"),
    ],
    "puffery": [
        (r"\bworld[- ]class\b", "unearned superlative"),
        (r"\bbest[- ]in[- ]class\b", "unearned superlative"),
        (r"\bindustry[- ]leading\b", "unearned superlative"),
        (r"\bstate[- ]of[- ]the[- ]art\b", "unearned superlative"),
        (r"\bnext[- ]gen(?:eration)?\b", "unearned superlative"),
        (r"\bunparall?ell?ed\b|\bunmatched\b|\bunrivall?ed\b|\bsecond to none\b", "unearned superlative"),
        (r"\brevolutionary\b|\bgroundbreaking\b|\bunprecedented\b", "unearned superlative"),
        (r"\blike never before\b", "unearned superlative"),
        (r"\bincredibly\b|\btruly\b|\bextremely\b|\bamazing(?:ly)?\b", "empty intensifier"),
    ],
    "attribution": [
        (r"\bstudies (?:show|have shown|suggest|prove|confirm)\b", "vague attribution"),
        (r"\bresearch (?:shows|has shown|suggests|proves|confirms)\b", "vague attribution"),
        (r"\bexperts (?:agree|say|believe|recommend|predict)\b", "vague attribution"),
        (r"\b(?:many|most|countless|numerous) (?:customers|users|people|experts|businesses|companies|teams|leaders) (?:say|agree|love|trust|believe|report)\b", "vague attribution"),
        (r"\bit is (?:widely|well|generally|commonly) (?:known|accepted|believed|recogni[sz]ed)\b", "vague attribution"),
        (r"\btrusted by (?:leading|top|the world's|thousands|millions|industry|the best|teams at)\b", "hollow proof"),
    ],
    "hedge": [
        (r"\b(?:may|might|could|can) potentially\b", "hedge stack"),
        (r"\b(?:could|might|may) possibly\b", "hedge stack"),
        (r"\bcan help (?:to )?\w+", "hedge (check whether commitment is warranted)"),
        (r"\b(?:may|might) help (?:to )?\w+", "hedge"),
        (r"\bit could be (?:said|argued)\b", "hedge"),
        (r"\bto (?:some|a certain) (?:extent|degree)\b", "hedge"),
    ],
    "significance": [
        (r"\bplays? an? (?:pivotal|crucial|vital|key|significant|important|critical) role\b", "inflated significance"),
        (r"\b(?:stands|serves) as an? (?:testament|reminder|beacon|example)\b", "inflated significance"),
        (r"\bmarks? an? (?:significant|major|key|pivotal|important|new) (?:milestone|moment|step|shift|chapter)\b", "inflated significance"),
        (r"\bunderscor(?:e|es|ed|ing) the (?:importance|need|significance|value)\b", "inflated significance"),
        (r"\bhighlight(?:s|ed|ing)? the (?:importance|significance)\b", "inflated significance"),
        (r"\breflects? an? (?:broader|deeper|growing) (?:trend|shift|commitment)\b", "inflated significance"),
        (r"\bin an era (?:of|where|when)\b|\bmore than ever\b", "inflated significance"),
    ],
    "agency": [
        (r"\bthe (?:data|numbers) (?:tells?|speaks?|shows? us)\b|\bthe numbers speak for themselves\b", "abstraction as actor"),
        (r"\b(?:innovation|technology|design|creativity|art|science) meets\b", "abstraction as actor"),
        (r"\bthis is where [\w' -]{1,30} comes? in\b", "abstraction as actor"),
        (r"\bthe (?:decision|answer|solution|path forward) (?:emerges|emerged)\b", "abstraction as actor"),
    ],
    # Claim candidates are not style problems. They are statements that need
    # checking against reference/claims.md: guarantees, superlatives,
    # unanchored comparisons, regulated words.
    "claim": [
        (r"\bguarantee[sd]?\b|\brisk[- ]free\b", "guarantee: needs terms or substantiation"),
        (r"\b(?:clinically|scientifically|medically) (?:proven|tested|validated)\b|\bproven to\b", "proof claim: needs a named study"),
        (r"\bthe only\b(?! (?:way|thing|time|one who|person|people|reason))|\bthe first (?:and only|to|ever|company|platform|app|product|brand|tool)\b|#1\b|\bnumber one\b|\bthe leading\b|\bcategory[- ]defining\b", "superlative: needs a stated basis"),
        (r"\bno (?:direct )?competit(?:ors|ion)\b", "competitive claim: needs a basis"),
        (r"\bup to \d[\d,.]*\s?(?:%|x|×|times)", "'up to' figure: is it typical?"),
        (r"\b\d[\d,.]*\s?(?:%|x|×|times) (?:more|less|faster|better|cheaper|higher|lower|returns?)\b", "comparison: needs a baseline"),
        (r"\b(?:100% )?(?:eco[- ]friendly|carbon[- ]neutral|net[- ]zero|biodegradable|sustainable|green)\b", "environmental claim: regulated, needs substantiation"),
        (r"\b(?:only \d+ (?:[\w-]+ ){0,2}(?:left|remaining|spots?|seats?)|offer ends|ends (?:at midnight|tonight|today)|last chance)\b", "urgency or scarcity: must be true"),
        (r"\brewires? (?:your|the) brain\b|\bboosts? (?:your )?(?:immunity|metabolism|concentration|focus)\b", "health claim: regulated, needs substantiation"),
    ],
    "ending": [
        (r"\bthe future is (?:bright|here|now)\b", "generic ending"),
        (r"\bexciting times (?:are )?ahead\b", "generic ending"),
        (r"\bonly time will tell\b", "generic ending"),
        (r"\bin conclusion\b|\bto sum (?:it )?up\b", "generic ending"),
        (r"\bultimately, (?:it's|this is|it is) (?:all )?about\b", "generic ending"),
        (r"\bthe possibilities are endless\b|\bthe sky's the limit\b", "generic ending"),
        (r"\bstay tuned\b", "generic ending"),
    ],
}

# Families that are usually deliberate in a given context profile. Hits in
# these families are reported under "suppressed" instead of "findings" so that
# judgment can still see them. Profile numbers follow reference/contexts.md.
CONTEXT_SUPPRESS = {
    "2": {"rhythm", "triplet", "agency"},          # brand manifesto
    "4": {"rhythm", "triplet", "agency"},          # advertising
    "5a": {"rhythm"},                              # headline
    "5b": {"rhythm", "agency"},                    # tagline
    "9": {"rhythm"},                               # social
    "10": {"throat", "rhythm"},                    # scripts (signposting is for the ear)
    "12": {"hedge"},                               # technical: qualifications are often required
    "13": {"format", "rhythm"},                    # long-form editorial
}

DASH_RE = re.compile(r"—|\s–\s|\s--\s")
WORD_RE = re.compile(r"[A-Za-z0-9À-ɏ]+(?:['’-][A-Za-z0-9À-ɏ]+)*")
TRIPLET_RE = re.compile(r"\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?,? (?:and|or) [\w-]+", re.IGNORECASE)
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'”’)\]]*\s+")
MD_NONPROSE_RE = re.compile(r"^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|\||>)")
BOLD_LABEL_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]{1,40}:?\*\*:?")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+(.+?)\s*#*\s*$")
SMALL_WORDS = {"a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to", "for", "by", "with", "vs", "via", "as", "is"}


def normalize(text):
    # HTML comments are not visible copy; blank them but keep line numbers.
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return (text.replace("‘", "'").replace("’", "'")
                .replace("“", '"').replace("”", '"'))


def line_col(text, index):
    line = text.count("\n", 0, index) + 1
    col = index - (text.rfind("\n", 0, index) + 1) + 1
    return line, col


def excerpt(text, start, end, width=60):
    a = max(0, start - width)
    b = min(len(text), end + width)
    snippet = text[a:b].replace("\n", " ").strip()
    return ("..." if a > 0 else "") + snippet + ("..." if b < len(text) else "")


def words(text):
    return WORD_RE.findall(text)


def prose_paragraphs(text):
    paras = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        prose = [ln for ln in lines if not MD_NONPROSE_RE.match(ln)]
        if prose:
            paras.append(" ".join(ln.strip() for ln in prose))
    return paras


def sentences(paragraph):
    return [s.strip() for s in SENT_SPLIT_RE.split(paragraph) if s.strip()]


def is_title_case(heading):
    toks = [t for t in re.findall(r"[A-Za-z][\w'-]*", heading)]
    if len(toks) < 3:
        return False
    content = [t for t in toks[1:] if t.lower() not in SMALL_WORDS]
    return bool(content) and all(t[0].isupper() for t in content)


def scan_phrases(text, families, allow):
    findings = []
    for family, patterns in families.items():
        for pattern, note in patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matched = m.group(0)
                if any(a and a in matched.lower() for a in allow):
                    continue
                line, col = line_col(text, m.start())
                findings.append({
                    "family": family,
                    "match": matched,
                    "line": line,
                    "col": col,
                    "excerpt": excerpt(text, m.start(), m.end()),
                    "note": note,
                })
    return findings


def scan_metrics(text):
    """Rhythm and format metrics. Returns (metrics, findings)."""
    findings = []
    total_words = len(words(text))
    paras = prose_paragraphs(text)
    all_sents = [s for p in paras for s in sentences(p)]
    lengths = [len(words(s)) for s in all_sents if words(s)]

    metrics = {
        "words": total_words,
        "sentences": len(lengths),
        "prose_paragraphs": len(paras),
        "mean_sentence_words": round(statistics.mean(lengths), 1) if lengths else 0,
        "sentence_length_cv": None,
        "dashes_per_100_words": 0.0,
        "triplets_per_100_words": 0.0,
        "question_ratio": 0.0,
    }

    def add(family, note, detail):
        findings.append({"family": family, "match": "", "line": None, "col": None,
                         "excerpt": detail, "note": note})

    # Sentence-length uniformity.
    if len(lengths) >= 6 and statistics.mean(lengths) > 0:
        cv = statistics.pstdev(lengths) / statistics.mean(lengths)
        metrics["sentence_length_cv"] = round(cv, 2)
        if cv < 0.3:
            add("rhythm", "uniform sentence length",
                "coefficient of variation %.2f across %d sentences (below 0.30 reads metronomic)" % (cv, len(lengths)))

    # Paragraphs that all end on a short punchline.
    multi = [sentences(p) for p in paras if len(sentences(p)) >= 2]
    if len(multi) >= 4:
        punch = [ss[-1] for ss in multi if len(words(ss[-1])) <= 6]
        ratio = len(punch) / len(multi)
        if ratio >= 0.6:
            add("rhythm", "paragraphs ending on a punchline",
                "%d of %d paragraphs end on a sentence of 6 words or fewer, e.g. \"%s\"" % (len(punch), len(multi), punch[0]))

    # Runs of dramatic fragments: three or more consecutive sentences of <= 3 words.
    for p in paras:
        ss = sentences(p)
        run = []
        for s in ss + [""]:
            if s and 0 < len(words(s)) <= 3:
                run.append(s)
                continue
            if len(run) >= 3:
                add("rhythm", "run of dramatic fragments", " ".join(run))
            run = []

    # Rhetorical questions.
    if lengths:
        q = sum(1 for s in all_sents if s.rstrip("\"')").endswith("?"))
        metrics["question_ratio"] = round(q / len(all_sents), 2) if all_sents else 0.0
        if q >= 3 and q / max(1, len(all_sents)) > 0.2:
            add("rhythm", "frequent rhetorical questions", "%d of %d sentences are questions" % (q, len(all_sents)))

    # Dash density.
    dashes = len(DASH_RE.findall(text))
    if total_words:
        density = dashes * 100.0 / total_words
        metrics["dashes_per_100_words"] = round(density, 2)
        if dashes >= 3 and density >= 1.0:
            add("format", "high dash density",
                "%d dashes in %d words (%.1f per 100). Density, not presence, is the signal." % (dashes, total_words, density))

    # Triplet density.
    trip = TRIPLET_RE.findall(" ".join(paras))
    if total_words:
        tdens = len(trip) * 100.0 / total_words
        metrics["triplets_per_100_words"] = round(tdens, 2)
        if len(trip) >= 3 and tdens >= 1.5:
            add("triplet", "reflexive triplets",
                "%d lists of three in %d words, e.g. \"%s\"" % (len(trip), total_words, trip[0]))

    # Formatting tells.
    lines = text.splitlines()
    bold_labels = [ln.strip() for ln in lines if BOLD_LABEL_RE.match(ln)]
    if len(bold_labels) >= 3:
        add("format", "bold-label bullets", "%d bullets start with a bold label, e.g. \"%s\"" % (len(bold_labels), bold_labels[0][:60]))
    headings = [m.group(1) for m in (HEADING_RE.match(ln) for ln in lines) if m]
    tc = [h for h in headings if is_title_case(h)]
    if len(headings) >= 3 and len(tc) / len(headings) >= 0.8:
        add("format", "title case on every heading", "%d of %d headings, e.g. \"%s\"" % (len(tc), len(headings), tc[0]))

    return metrics, findings


def run(text, context=None, avoid=None, allow=None):
    text = normalize(text)
    allow = [a.strip().lower() for a in (allow or []) if a.strip()]
    families = dict(FAMILIES)
    if avoid:
        families["brand-avoid"] = [
            (r"\b" + re.escape(w.strip()) + r"\b" if re.match(r"^[\w ]+$", w.strip()) else re.escape(w.strip()),
             "listed under 'we don't say' in BRAND.md")
            for w in avoid if w.strip()
        ]

    findings = scan_phrases(text, families, allow)
    metrics, metric_findings = scan_metrics(text)
    findings.extend(metric_findings)

    suppress = CONTEXT_SUPPRESS.get(str(context), set()) if context else set()
    active = [f for f in findings if f["family"] not in suppress]
    suppressed = {}
    for f in findings:
        if f["family"] in suppress:
            suppressed[f["family"]] = suppressed.get(f["family"], 0) + 1

    summary = {}
    for f in active:
        summary[f["family"]] = summary.get(f["family"], 0) + 1

    active.sort(key=lambda f: (f["line"] is None, f["line"] or 0, f["col"] or 0))
    return {
        "tool": "copy-tells",
        "version": "0.1.0",
        "context": context,
        "note": "Evidence, not verdict. Confirm each hit against reference/tells.md calibration before reporting.",
        "metrics": metrics,
        "summary": summary,
        "suppressed": suppressed,
        "findings": active,
    }


def render_text(result):
    out = []
    m = result["metrics"]
    out.append("copy-tells %s  context=%s" % (result["version"], result["context"] or "none"))
    out.append("words=%d sentences=%d mean_len=%s cv=%s dashes/100w=%s triplets/100w=%s"
               % (m["words"], m["sentences"], m["mean_sentence_words"], m["sentence_length_cv"],
                  m["dashes_per_100_words"], m["triplets_per_100_words"]))
    if not result["findings"]:
        out.append("No candidate patterns found.")
    for f in result["findings"]:
        loc = "L%d:%d" % (f["line"], f["col"]) if f["line"] else "doc"
        what = ('"%s"' % f["match"]) if f["match"] else ""
        out.append("[%s] %s %s %s\n    %s" % (f["family"], loc, what, "(" + f["note"] + ")", f["excerpt"]))
    if result["suppressed"]:
        out.append("Suppressed for this context: " + ", ".join("%s=%d" % kv for kv in sorted(result["suppressed"].items())))
    out.append(result["note"])
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="COPY tells linter (evidence, not verdict).")
    ap.add_argument("path", help="file to scan, or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--context", help="context profile number from reference/contexts.md (e.g. 3, 5a, 12)")
    ap.add_argument("--avoid", default="", help="comma-separated brand-banned words or phrases")
    ap.add_argument("--allow", default="", help="comma-separated brand vocabulary to ignore")
    args = ap.parse_args(argv)

    try:
        if args.path == "-":
            data = sys.stdin.buffer.read().decode("utf-8", errors="replace")
        else:
            with open(args.path, "r", encoding="utf-8", errors="replace") as fh:
                data = fh.read()
    except OSError as exc:
        sys.stderr.write("copy-tells: cannot read %s: %s\n" % (args.path, exc))
        return 1

    result = run(data, context=args.context,
                 avoid=args.avoid.split(",") if args.avoid else None,
                 allow=args.allow.split(",") if args.allow else None)

    out = json.dumps(result, indent=2, ensure_ascii=False) if args.json else render_text(result)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    sys.stdout.write(out + "\n")
    return 2 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
