# word-count-cli

Count lines, words and characters in text files — a small `wc`-style tool
with a friendlier table output and a JSON mode. Stdlib-only Python, no
dependencies.

## What it does

- Counts **lines**, **words** and **characters** per file, plus a TOTAL row.
- Lines: newline-terminated lines; a trailing partial line counts as 1.
- Words: whitespace-separated tokens. Chars: Unicode characters, newlines included.
- `--json` prints machine-readable output; `--stdin` reads piped text.
- The same file listed twice is counted once.
- Reads files as UTF-8, tolerating undecodable bytes.

## How to run

```bash
python word_count.py notes.txt
python word_count.py a.txt b.txt --json
echo "hello world" | python word_count.py --stdin
```

Requires Python 3.8+.

## Example output

One file (`sample.txt` contains `Hello world` and `This is a test.` on two lines):

```
FILE        LINES  WORDS  CHARS
-------------------------------
sample.txt   2   6  28
TOTAL        2   6  28
```

Several files at once:

```
FILE        LINES  WORDS  CHARS
-------------------------------
sample.txt   2   6  28
single.txt   1   7  32
empty.txt    0   0   0
TOTAL        3  13  60
```

JSON mode (`python word_count.py sample.txt --json`):

```json
{
  "files": [
    {
      "file": "sample.txt",
      "lines": 2,
      "words": 6,
      "chars": 28
    }
  ],
  "total": {
    "lines": 2,
    "words": 6,
    "chars": 28
  }
}
```

Piped input (`echo "hello world" | python word_count.py --stdin`):

```
FILE     LINES  WORDS  CHARS
----------------------------
<stdin>   1   2  12
TOTAL     1   2  12
```

## Exit codes

| Code | Meaning |
| ---- | ------- |
| 0 | OK |
| 1 | A listed file could not be read (message printed to stderr) |
| 2 | Usage error (no files given and no `--stdin`, or `--stdin` with files) |
