#!/usr/bin/env python3
"""Heuristic ASD-STE100 (Simplified Technical English) checker for Markdown files.

Checks prose and code comments (not code) for:
    - sentence length (20 words procedural, 25 words descriptive)
    - paragraph length (6 sentences)
    - passive voice, -ing verb forms, unapproved words, contractions, semicolons

It is a heuristic: it cannot understand meaning, so treat each flag as a
question for a human/LLM reviewer, not a final verdict.

Usage:
    python3 ste_check.py FILE.md [--max-procedural 20] [--max-descriptive 25]

Exit code: 0 = no errors (warnings may remain), 1 = errors found, 2 = bad usage.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Unapproved word -> STE replacement (see references/ste-rules.md section 10).
UNAPPROVED = {
    "utilize": "use", "utilise": "use", "employ": "use",
    "perform": "do", "ensure": "make sure", "verify": "make sure / check",
    "confirm": "make sure / check", "commence": "start", "initiate": "start",
    "terminate": "stop / end", "obtain": "get", "acquire": "get",
    "require": "need", "requires": "needs", "assist": "help",
    "attempt": "try", "numerous": "many", "sufficient": "enough",
    "additional": "more", "locate": "find", "modify": "change",
    "indicate": "show", "indicates": "shows", "demonstrate": "show",
    "determine": "find / calculate", "facilitate": "help",
    "basically": "(delete)", "simply": "(delete)", "just": "(delete)",
    "actually": "(delete)", "really": "(delete)", "easy": "(delete)",
    "easily": "(delete)", "obviously": "(delete)", "should": "must / imperative",
    "might": "can / may", "roughly": "about",
}
UNAPPROVED_PHRASES = {
    "prior to": "before", "subsequent to": "after", "in order to": "to",
    "due to": "because of", "a lot of": "many", "lots of": "many",
    "adjacent to": "near / next to", "of course": "(delete)",
    "make sure that": "make sure", "you should": "imperative verb",
}

# -ing words that are not verb forms (nouns, prepositions, technical names).
ING_ALLOW = {
    "string", "strings", "thing", "things", "something", "anything", "nothing",
    "everything", "during", "bring", "spring", "ring", "king", "wing", "sing",
    "ceiling", "wiring", "heading", "headings", "setting", "settings",
    "debouncing", "building", "morning", "evening", "awning", "padding",
    "spacing", "timing", "housing", "bearing", "coupling", "fitting", "o-ring",
    "ping", "sling", "swing", "duckling", "pudding", "missing", "warning", "warnings",
}

BE_VERBS = r"(?:is|are|was|were|be|been|being|am)"
IRREGULAR_PARTICIPLES = (
    "built|done|made|sent|set|shown|given|taken|written|held|kept|put|read|"
    "found|known|seen|run|cut|left|lost|sold|told|bound|brought|caught|chosen|"
    "drawn|driven|fed|hidden|laid|led|meant|paid|shut|spent|split|struck|thrown"
)
PASSIVE_RE = re.compile(
    rf"\b{BE_VERBS}\s+(?:\w+ly\s+)?(\w+ed|{IRREGULAR_PARTICIPLES})\b", re.IGNORECASE
)
CONTRACTION_RE = re.compile(
    r"\b\w+(?:n't|'re|'ll|'ve|'d|'m)\b|\b(?:it|that|there|what|here|who|he|she)'s\b",
    re.IGNORECASE,
)
ING_RE = re.compile(r"\b[a-zA-Z]{3,}ing\b")
# Comment markers for Python/Bash (#) and PowerShell (#, <# #>).
CODE_COMMENT_RE = re.compile(r"(?:^|\s)#\s?(.*)$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`\"'(*])")


@dataclass
class Issue:
    line: int
    level: str  # "ERROR" or "WARN"
    rule: str
    text: str


def strip_markdown(text: str) -> str:
    """Remove inline Markdown so that only words are left to count."""
    text = re.sub(r"`[^`]*`", "CODE", text)               # inline code -> one word
    text = re.sub(r"!?\[([^\]]*)\]\[[^\]]*\]", r"\1", text)  # reference links
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)   # inline links
    text = re.sub(r"https?://\S+", "URL", text)
    text = re.sub(r"[*_>#]+", " ", text)
    return text.strip()


def word_count(sentence: str) -> int:
    return len([w for w in re.split(r"\s+", sentence) if re.search(r"\w", w)])


def extract_blocks(lines):
    """Yield (line_no, text, kind, paragraph_id) for prose and code comments.

    kind is "procedural" (numbered list items), "descriptive", or "comment".
    """
    in_fence = False
    fence_lang = ""
    paragraph_id = 0
    for number, raw in enumerate(lines, start=1):
        raw = re.sub(r"^\s*>\s?", "", raw)  # check blockquote content as normal text
        stripped = raw.strip()
        fence = re.match(r"^(```|~~~)\s*(\w*)", stripped)
        if fence:
            in_fence = not in_fence
            fence_lang = fence.group(2).lower() if in_fence else ""
            paragraph_id += 1
            continue
        if in_fence:
            # Diagrams and plain text blocks are not checked; code comments are.
            if fence_lang in ("python", "py", "bash", "sh", "shell", "powershell", "ps1", "pwsh"):
                match = CODE_COMMENT_RE.search(raw)
                if match and not stripped.startswith("#!") and match.group(1).strip():
                    yield number, match.group(1).strip(), "comment", None
            continue
        if not stripped:
            paragraph_id += 1
            continue
        # Skip headings, tables, link definitions, HTML, front matter separators.
        if stripped.startswith(("#", "|", "<", "---")) or re.match(r"^\[[^\]]+\]:", stripped):
            paragraph_id += 1
            continue
        kind = "procedural" if re.match(r"^\d+[.)]\s", stripped) else "descriptive"
        if re.match(r"^[-*+]\s|^\d+[.)]\s", stripped):
            paragraph_id += 1  # each list item is its own paragraph
        yield number, strip_markdown(re.sub(r"^(?:[-*+]|\d+[.)])\s+(\[.\]\s+)?", "", stripped)), kind, paragraph_id


def check(path: Path, max_proc: int, max_desc: int):
    lines = path.read_text(encoding="utf-8").splitlines()
    issues: list[Issue] = []
    paragraph_sentences: dict[int, tuple[int, int]] = {}  # id -> (first line, count)

    for number, text, kind, paragraph_id in extract_blocks(lines):
        sentences = [s for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
        if paragraph_id is not None and kind == "descriptive":
            first, count = paragraph_sentences.get(paragraph_id, (number, 0))
            paragraph_sentences[paragraph_id] = (first, count + len(sentences))

        for sentence in sentences:
            words = word_count(sentence)
            limit = max_proc if kind in ("procedural", "comment") else max_desc
            if words > limit:
                issues.append(Issue(number, "ERROR", f"sentence > {limit} words ({words})", sentence))

            lower = sentence.lower()
            for match in PASSIVE_RE.finditer(sentence):
                level = "ERROR" if kind == "procedural" else "WARN"
                issues.append(Issue(number, level, "passive voice?", match.group(0)))
            for match in ING_RE.finditer(sentence):
                if match.group(0).lower() not in ING_ALLOW:
                    issues.append(Issue(number, "WARN", "-ing form?", match.group(0)))
            for word in re.findall(r"[a-zA-Z']+", lower):
                if word in UNAPPROVED:
                    issues.append(Issue(number, "ERROR", "unapproved word", f"{word} -> {UNAPPROVED[word]}"))
            for phrase, replacement in UNAPPROVED_PHRASES.items():
                if re.search(rf"\b{phrase}\b", lower):
                    issues.append(Issue(number, "ERROR", "unapproved phrase", f"{phrase} -> {replacement}"))
            for match in CONTRACTION_RE.finditer(sentence):
                issues.append(Issue(number, "ERROR", "contraction", match.group(0)))
            if ";" in sentence:
                issues.append(Issue(number, "ERROR", "semicolon", sentence[:60]))

    for first, count in paragraph_sentences.values():
        if count > 6:
            issues.append(Issue(first, "ERROR", f"paragraph > 6 sentences ({count})", ""))

    return sorted(issues, key=lambda issue: issue.line)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", type=Path)
    parser.add_argument("--max-procedural", type=int, default=20)
    parser.add_argument("--max-descriptive", type=int, default=25)
    args = parser.parse_args()
    if not args.file.is_file():
        print(f"error: {args.file} is not a file", file=sys.stderr)
        return 2

    issues = check(args.file, args.max_procedural, args.max_descriptive)
    for issue in issues:
        detail = f": {issue.text}" if issue.text else ""
        print(f"{args.file}:{issue.line}: {issue.level} {issue.rule}{detail}")

    errors = sum(issue.level == "ERROR" for issue in issues)
    warnings = len(issues) - errors
    print(f"\nSTE check: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
