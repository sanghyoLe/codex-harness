#!/usr/bin/env python3
"""Find the closest harnesses in codex-harness-100 for a free-text query."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CANDIDATE_ROOTS = [
    Path("/Users/isanghyo/Desktop/harness/codex-harness-100"),
    Path("/Users/isanghyo/Desktop/codex-harness-100"),
    SCRIPT_DIR.parents[5] / "codex-harness-100",
    Path.cwd() / "codex-harness-100",
]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9가-힣]+", text.lower())


def resolve_default_root() -> Path:
    for root in CANDIDATE_ROOTS:
        if root.exists():
            return root
    return CANDIDATE_ROOTS[0]


def load_harnesses(root: Path, language: str) -> list[dict]:
    languages = [language] if language in {"ko", "en"} else ["ko", "en"]
    harnesses: list[dict] = []

    for lang in languages:
        lang_root = root / lang
        if not lang_root.exists():
            continue
        for agents_path in sorted(lang_root.glob("*/AGENTS.md")):
            harness_dir = agents_path.parent
            text = agents_path.read_text()
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            title = lines[0].lstrip("# ").strip() if lines else harness_dir.name
            summary = lines[1] if len(lines) > 1 else ""
            blob = " ".join(lines[:80])
            harnesses.append(
                {
                    "language": lang,
                    "slug": harness_dir.name,
                    "path": str(harness_dir),
                    "title": title,
                    "summary": summary,
                    "blob": blob,
                }
            )
    return harnesses


def score(query_tokens: list[str], harness: dict) -> tuple[int, list[str]]:
    text_tokens = set(tokenize(" ".join([harness["slug"], harness["title"], harness["summary"], harness["blob"]])))
    slug_tokens = set(tokenize(harness["slug"].replace("-", " ")))
    matched: list[str] = []
    total = 0
    for token in query_tokens:
        if token in slug_tokens:
            total += 5
            matched.append(token)
        elif token in text_tokens:
            total += 2
            matched.append(token)
    return total, sorted(set(matched))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find similar harnesses in codex-harness-100.")
    parser.add_argument("query", help="Free-text search query")
    parser.add_argument("--root", default=str(resolve_default_root()), help="Path to codex-harness-100")
    parser.add_argument("--language", choices=["ko", "en", "all"], default="all")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser()
    harnesses = load_harnesses(root, args.language)
    query_tokens = tokenize(args.query)

    ranked = []
    for harness in harnesses:
        value, matched = score(query_tokens, harness)
        if value <= 0:
            continue
        ranked.append(
            {
                "score": value,
                "matched_tokens": matched,
                "language": harness["language"],
                "slug": harness["slug"],
                "path": harness["path"],
                "title": harness["title"],
                "summary": harness["summary"],
            }
        )

    ranked.sort(key=lambda item: (-item["score"], item["language"], item["slug"]))
    ranked = ranked[: args.limit]

    if args.json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2))
        return

    if not ranked:
        print("No matching harnesses found.")
        return

    for index, item in enumerate(ranked, start=1):
        matched = ", ".join(item["matched_tokens"]) or "-"
        print(f"{index}. [{item['language']}] {item['slug']}  score={item['score']}")
        print(f"   title: {item['title']}")
        print(f"   path: {item['path']}")
        print(f"   matched: {matched}")
        print(f"   summary: {item['summary']}")


if __name__ == "__main__":
    main()
