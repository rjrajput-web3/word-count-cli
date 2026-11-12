#!/usr/bin/env python3
"""word-count-cli — count lines, words and characters in text files.

A small `wc`-style tool with a friendlier table output and JSON mode:

    python word_count.py notes.txt
    python word_count.py a.txt b.txt --json
    echo "hello world" | python word_count.py --stdin

Counts:
- lines: newline-terminated lines (a trailing partial line counts as 1)
- words: whitespace-separated tokens
- chars: Unicode characters, including newlines

Exit codes: 0 = OK, 1 = a listed file could not be read, 2 = usage error.
Only the Python standard library is used.
"""

import argparse
import json
import sys


def count_text(text):
    """Return (lines, words, chars) for one string."""
    chars = len(text)
    words = len(text.split())
    if not text:
        lines = 0
    else:
        lines = text.count("\n")
        if not text.endswith("\n"):
            lines += 1
    return lines, words, chars


def read_file(path):
    """Read a file as UTF-8, tolerating undecodable bytes."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def format_table(results, totals):
    """Render one aligned table row per file plus a total row."""
    rows = [(name, l, w, c) for name, (l, w, c) in results]
    rows.append(("TOTAL", totals[0], totals[1], totals[2]))
    name_w = max(len(r[0]) for r in rows)
    num_w = max(len(str(r[i])) for r in rows for i in (1, 2, 3))
    header = f"{'FILE':<{name_w}}  {'LINES':>{num_w}}  {'WORDS':>{num_w}}  {'CHARS':>{num_w}}"
    sep = "-" * len(header)
    lines = [header, sep]
    for name, l, w, c in rows:
        lines.append(f"{name:<{name_w}}  {l:>{num_w}}  {w:>{num_w}}  {c:>{num_w}}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Count lines, words and characters in text files."
    )
    parser.add_argument("files", nargs="*", help="files to count")
    parser.add_argument("--stdin", action="store_true",
                        help="read text from stdin instead of files")
    parser.add_argument("--json", action="store_true",
                        help="print results as JSON instead of a table")
    args = parser.parse_args(argv)

    if args.stdin and args.files:
        parser.error("--stdin cannot be combined with file arguments")
    if not args.stdin and not args.files:
        parser.error("give one or more files, or use --stdin")

    results = []  # list of (name, (lines, words, chars))
    had_error = False

    if args.stdin:
        text = sys.stdin.read()
        results.append(("<stdin>", count_text(text)))
    else:
        seen = set()
        for path in args.files:
            if path in seen:
                continue
            seen.add(path)
            try:
                results.append((path, count_text(read_file(path))))
            except OSError as exc:
                print(f"word_count.py: {path}: {exc.strerror}", file=sys.stderr)
                had_error = True

    if not results:
        if not had_error:
            print("No files to count.")
        return 1 if had_error else 0

    totals = tuple(sum(r[1][i] for r in results) for i in range(3))

    if args.json:
        payload = {
            "files": [
                {"file": name, "lines": l, "words": w, "chars": c}
                for name, (l, w, c) in results
            ],
            "total": {"lines": totals[0], "words": totals[1], "chars": totals[2]},
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_table(results, totals))

    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
