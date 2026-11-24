#!/usr/bin/env python3
"""One Word for Your Wi-Fi — entry program (program/v1, python3.13).

Writes a single word to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt).

The word is picked by scoring a shortlist of candidates against the judge's
published brief, in the brief's own order of importance:

  1. on-subject fit — describes Wi-Fi as the entrant actually lives it
  2. funny at once — a real laugh, no explanation needed
  3. true — recognisable home-Wi-Fi behaviour
  4. fresh — not the word everyone reaches for
  5. instant — one word, understood with no context

The pick: "Catfishing".

Why it wins: home Wi-Fi constantly shows full bars and "Connected" while
delivering no internet at all — it lured you in with a fake profile, then
nothing behind it. The joke lands in one beat, it is true of every router
that has ever lied about its signal, and nobody in the field is using it
(the crowd is piled onto "Gaslighting" and "Ghosting", which score near-zero
on freshness). 10 characters, inside the 1-20 gate, no trailing newline so
the file is exactly the word.
"""

import os
import sys

# Candidate words, each scored 0-5 on the judge's five criteria in order:
# (fit, laugh, truth, fresh, instant). Scores are the builder's judgement
# from the published brief and a scan of the field's submitted titles.
CANDIDATES = [
    # word,           fit, laugh, truth, fresh, instant
    ("Catfishing",    5,   5,     5,     5,     5),
    ("Gaslighting",   5,   4,     5,     1,     5),
    ("Ghosting",      4,   4,     4,     1,     5),
    ("Breadcrumbing", 4,   4,     4,     3,     3),
    ("Narcoleptic",   4,   4,     4,     4,     3),
    ("Situationship", 4,   4,     4,     2,     4),
    ("Peekaboo",      3,   3,     3,     2,     5),
    ("Flaky",         4,   2,     4,     1,     5),
]

# Weights follow the brief's order: fit matters most, instant least.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    """Weighted score; ties break to the shorter word, then alphabetical."""
    _, *marks = candidate
    return sum(w * m for w, m in zip(WEIGHTS, marks))


def pick_word(candidates):
    """Return the best word. Deterministic: no randomness, no input."""
    ranked = sorted(candidates, key=lambda c: (-score(c), len(c[0]), c[0]))
    return ranked[0][0]


def validate(word):
    """The gate: UTF-8 text, 1-20 characters, not only whitespace, one word."""
    if not word or word != word.strip():
        raise ValueError("word must be non-empty with no surrounding space")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word")
    if not 1 <= len(word) <= 20:
        raise ValueError("word must be 1-20 characters")
    word.encode("utf-8")  # raises if not encodable
    return word


def main():
    word = validate(pick_word(CANDIDATES))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exactly the word: no trailing newline, so the file is 10 bytes.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    print(f"wrote {path}: {word!r} ({len(word)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
