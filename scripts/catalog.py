#!/usr/bin/env python3
"""Look up installed Heiyao character LoRA prompt records."""
import argparse
import json
import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
PUBLIC_CATALOG = SKILL / "references" / "characters.json"
PROJECT = SKILL.parent.parent.parent
LOCAL_CATALOG = PROJECT / ".agents" / "state" / "heiyao-prompts" / "catalog.json"


def normalized(value):
    return re.sub(r"[\s_+\-·.]+", "", value).casefold()


def load_records(path):
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("characters"), list):
        raise ValueError("Unsupported character catalog format")
    return payload["characters"]


def matching(rows, term, exact, filters):
    needle = normalized(term)
    if not needle:
        return []
    matched = []
    for row in rows:
        if any(value and normalized(row.get(field, "")) != normalized(value)
               for field, value in filters.items()):
            continue
        fields = [row["name"], row["trigger"], *row.get("aliases", [])]
        if not exact:
            fields.extend([row["work"], row["base"]])
        if any(needle == normalized(field) if exact else needle in normalized(field)
               for field in fields):
            matched.append(row)
    trigger_matches = [row for row in matched if needle == normalized(row["trigger"])]
    if exact and trigger_matches:
        return trigger_matches
    if exact and any(not row.get("source_only") for row in matched):
        return [row for row in matched if not row.get("source_only")]
    return matched


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["query", "search"])
    parser.add_argument("terms", nargs="+")
    parser.add_argument("--work")
    parser.add_argument("--base")
    parser.add_argument("--version")
    parser.add_argument("--public", action="store_true", help="Use the distributed catalog only")
    args = parser.parse_args()

    local = SKILL.parent.name == "skills" and SKILL.parent.parent.name == ".agents" and LOCAL_CATALOG.is_file()
    path = LOCAL_CATALOG if local and not args.public else PUBLIC_CATALOG
    rows = load_records(path)
    filters = {"work": args.work, "base": args.base, "version": args.version}
    exact = args.command == "query"
    results = []
    for term in args.terms:
        candidates = matching(rows, term, exact, filters)
        preferred = [row for row in candidates if row.get("default")]
        if len(candidates) == 1:
            default = candidates[0]
        elif len(preferred) == 1 and len({row["work"] for row in candidates}) == 1:
            default = preferred[0]
        else:
            default = None
        if not exact:
            candidates = [{field: row[field] for field in ("work", "name", "base", "version", "trigger")}
                          for row in candidates]
        source_only = default and default.get("source_only")
        results.append({
            "term": term,
            "status": ("no_match" if not candidates else "source_only" if source_only else
                       "resolved" if default else "choose_version")
                       if exact else "matches",
            "preferred_version": ({"work": default["work"], "name": default["name"],
                                   "base": default["base"], "version": default["version"],
                                   "trigger": default["trigger"]} if exact and default and not source_only else None),
            "candidates": candidates,
        })
    print(json.dumps({"catalog": "local" if path == LOCAL_CATALOG else "public",
                      "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
