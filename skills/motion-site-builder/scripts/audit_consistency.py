#!/usr/bin/env python3
"""Cross-file motion consistency audit — the drift layer a per-file linter can't see.

Inventories every animation duration, easing curve, and spring config across a
source tree, then reports value drift (many near-identical values that should be
tokens) and exit-risk files (Framer Motion conditional mounts with no
AnimatePresence). Companion to lint_motion.py (per-file rules M01-M20); used by
the improve-motion audit (AUDIT.md §7 Cohesion & tokens).

Usage:
    python3 audit_consistency.py <src-dir> [--json]
    MOTION_PROFILE=product-ui python3 audit_consistency.py <src-dir>
    python3 audit_consistency.py --self-test

Zero dependencies. Exit code 0 on a successful run (it reports; humans decide);
non-zero only on invalid usage (e.g. the path is not a directory).
"""

import json
import os
import re
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTS = (".css", ".scss", ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte")
SKIP_DIRS = {"node_modules", "dist", "build", ".git", ".next", "coverage", "out"}

# Drift thresholds (heuristic, from the audit playbook)
MAX_DISTINCT_DURATIONS = 8
MAX_DISTINCT_EASINGS = 5

# CSS declarations are parsed as complete comma-separated lists. In a shorthand,
# the first time in EACH list item is the duration and the second is the delay.
# `*-delay` declarations are deliberately outside this regex.
RE_CSS_TIME_DECL = re.compile(
    r"(?<![\w-])(?:transition|animation)(?P<longhand>-duration)?\s*:\s*(?P<value>[^;{}]+)"
)
RE_TIME_LITERAL = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(ms|s)\b")
RE_FRAMER_DURATION = re.compile(r"duration\s*[:=]\s*(\d+(?:\.\d+)?)")
RE_BEZIER = re.compile(r"cubic-bezier\(\s*[^)]+\)")
RE_EASE_KEYWORD = re.compile(
    r"(?<![-\w])(ease-in-out|ease-in|ease-out|linear|ease)(?![-\w(])"
)
RE_CSS_EASING_DECL = re.compile(
    r"(?<![\w-])(?:transition|animation)(?:-timing-function)?\s*:\s*(?P<value>[^;{}]+)"
)
RE_FRAMER_EASE_STR = re.compile(r"ease\s*[:=]\s*[\"']([a-zA-Z_-]+)[\"']")
RE_FRAMER_EASE_ARRAY = re.compile(r"ease\s*[:=]\s*\[([^\]]+)\]")
RE_FRAMER_EASE_IDENT = re.compile(r"ease\s*[:=]\s*([A-Za-z_][A-Za-z0-9_]*)\b")
RE_SPRING = re.compile(
    r"stiffness\s*[:=]\s*(\d+(?:\.\d+)?)[^}]*?damping\s*[:=]\s*(\d+(?:\.\d+)?)", re.S
)
RE_CONDITIONAL_MOTION = re.compile(r"\{[^}]*(?:&&|\?)\s*<\s*motion\.")
# Any of these in a file counts as an exit mechanism for the exit-risk heuristic
# (per interaction-standards §5: AnimatePresence OR CSS @starting-style / mounted flag).
EXIT_MECHANISMS = ("AnimatePresence", "@starting-style", "data-mounted")


def norm_easing(value):
    value = value.strip().lower()
    if value.startswith("cubic-bezier"):
        return re.sub(r"\s+", "", value)
    aliases = {
        "easein": "ease-in",
        "easeout": "ease-out",
        "easeinout": "ease-in-out",
    }
    return aliases.get(re.sub(r"[-_]", "", value), value)


def load_token_easings():
    """Easing values from the active profile so token matches can be marked."""
    profile = os.environ.get("MOTION_PROFILE", "cinematic")
    if profile == "cinematic":
        path = os.path.join(SCRIPT_DIR, "..", "config", "motion-tokens.json")
    else:
        path = os.path.join(SCRIPT_DIR, "..", "config", "profiles", profile + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            easings = json.load(f).get("easings", {})
        return {norm_easing(v) for v in easings.values() if isinstance(v, str)}
    except (OSError, ValueError):
        return set()


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(EXTS):
                yield os.path.join(dirpath, name)


def norm_duration(value, unit):
    ms = float(value) * (1000 if unit == "s" else 1)
    # The prefers-reduced-motion boilerplate (0.01ms resets, mandated by M01)
    # is compliance, not drift — never inventory it.
    if ms <= 0.02:
        return None
    return f"{ms:g}ms"


def split_css_list(value):
    """Split a CSS comma-list without splitting inside functions or strings.

    Returns `(item, start_offset)` pairs so callers can preserve source lines.
    """
    parts = []
    depth = 0
    quote = None
    start = 0
    escaped = False
    for i, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote:
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            parts.append((value[start:i], start))
            start = i + 1
    parts.append((value[start:], start))
    return parts


def extract_css_durations(text):
    """Yield `(normalized_duration, absolute_offset)` for CSS declarations."""
    for declaration in RE_CSS_TIME_DECL.finditer(text):
        value = declaration.group("value")
        for item, item_offset in split_css_list(value):
            times = list(RE_TIME_LITERAL.finditer(item))
            if not times:
                continue
            # Longhand items contain one duration; shorthand items may contain a
            # second time, which is delay and must not enter the inventory.
            duration = times[0]
            key = norm_duration(duration.group(1), duration.group(2))
            if key:
                yield key, declaration.start("value") + item_offset + duration.start()


def extract_css_easings(text):
    """Yield `(normalized_easing, absolute_offset)` from CSS motion declarations."""
    for declaration in RE_CSS_EASING_DECL.finditer(text):
        value = declaration.group("value")
        for match in RE_BEZIER.finditer(value):
            yield norm_easing(match.group(0)), declaration.start("value") + match.start()
        for match in RE_EASE_KEYWORD.finditer(value):
            yield match.group(1), declaration.start("value") + match.start()


def resolve_ease_constants(text):
    """Resolve typed/untyped numeric array constants used as Framer easings."""
    return {
        m.group(1): "cubic-bezier(" + re.sub(r"\s+", "", m.group(2)) + ")"
        for m in re.finditer(
            r"(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?::[^=]*)?=\s*\[([^\]]+)\]",
            text,
        )
    }


def audit(root):
    durations = defaultdict(list)   # "300ms" -> [file:line, ...]
    easings = defaultdict(list)     # normalized curve/keyword -> [file:line, ...]
    springs = defaultdict(list)     # "stiffness/damping" -> [file:line, ...]
    exit_risk = []                  # files with conditional <motion.*> and no AnimatePresence

    for path in iter_files(root):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except OSError:
            continue
        rel = os.path.relpath(path, root)
        is_jsx = path.endswith((".tsx", ".jsx", ".js", ".ts"))

        ease_consts = resolve_ease_constants(text) if is_jsx else {}

        for key, offset in extract_css_durations(text):
            durations[key].append(f"{rel}:{text.count(chr(10), 0, offset) + 1}")
        for key, offset in extract_css_easings(text):
            easings[key].append(f"{rel}:{text.count(chr(10), 0, offset) + 1}")

        for i, line in enumerate(text.splitlines(), 1):
            loc = f"{rel}:{i}"
            if is_jsx:
                for m in RE_FRAMER_DURATION.finditer(line):
                    v = float(m.group(1))
                    if 0 < v <= 10:  # Framer durations are seconds; skip unrelated numbers
                        key = norm_duration(m.group(1), "s")
                        if key:
                            durations[key].append(loc)
                for m in RE_FRAMER_EASE_STR.finditer(line):
                    easings[norm_easing(m.group(1))].append(loc)
                for m in RE_FRAMER_EASE_ARRAY.finditer(line):
                    easings["cubic-bezier(" + re.sub(r"\s+", "", m.group(1)) + ")"].append(loc)
                for m in RE_FRAMER_EASE_IDENT.finditer(line):
                    name = m.group(1)
                    easings[ease_consts.get(name, f"const:{name}")].append(loc)

        for m in RE_SPRING.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            springs[f"stiffness {m.group(1)} / damping {m.group(2)}"].append(f"{rel}:{line_no}")

        if (is_jsx and RE_CONDITIONAL_MOTION.search(text)
                and not any(k in text for k in EXIT_MECHANISMS)):
            exit_risk.append(rel)

    return durations, easings, springs, exit_risk


def self_test():
    sample = """
    .a {
      transition: opacity 200ms ease 900ms, transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
      animation: fade 400ms ease-out 100ms, slide 0.5s linear 50ms;
      transition-duration: 600ms, 0.7s;
      animation-delay: 8s;
    }
    """
    durations = [value for value, _offset in extract_css_durations(sample)]
    easings = [value for value, _offset in extract_css_easings(sample)]
    typed = "const EXPO: [number, number, number, number] = [0.16, 1, 0.3, 1]"
    checks = {
        "all-comma-list-durations": durations == ["200ms", "300ms", "400ms", "500ms", "600ms", "700ms"],
        "delays-excluded": "900ms" not in durations and "8000ms" not in durations,
        "easings-extracted-once": easings == ["cubic-bezier(0.16,1,0.3,1)", "ease", "ease-out", "linear"],
        "typed-easing-constant": resolve_ease_constants(typed).get("EXPO") == "cubic-bezier(0.16,1,0.3,1)",
        "framer-easing-alias": norm_easing("easeOut") == "ease-out",
    }
    print(json.dumps({"checks": checks, "pass": all(checks.values())}, indent=2))
    return 0 if all(checks.values()) else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    root = args[0] if args else "."
    if not os.path.isdir(root):
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    durations, easings, springs, exit_risk = audit(root)
    token_easings = load_token_easings()
    off_token = sorted(k for k in easings
                       if ((k.startswith("cubic-bezier") and k not in token_easings)
                           or k.startswith("const:")))

    report = {
        "root": os.path.abspath(root),
        "profile": os.environ.get("MOTION_PROFILE", "cinematic"),
        "distinct_durations": len(durations),
        "distinct_easings": len(easings),
        "duration_drift": len(durations) > MAX_DISTINCT_DURATIONS,
        "easing_drift": len(off_token) > MAX_DISTINCT_EASINGS,
        "durations": {k: {"count": len(v), "sample": v[:3]}
                      for k, v in sorted(durations.items(), key=lambda kv: -len(kv[1]))},
        "easings": {k: {"count": len(v), "sample": v[:3], "token": k in token_easings}
                    for k, v in sorted(easings.items(), key=lambda kv: -len(kv[1]))},
        "off_token_beziers": [k for k in off_token if k.startswith("cubic-bezier")],
        "off_token_easings": off_token,
        "springs": {k: {"count": len(v), "sample": v[:3]} for k, v in springs.items()},
        "exit_risk_files": exit_risk,
    }

    if as_json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"Motion consistency audit — {report['root']} (profile: {report['profile']})\n")
    print(f"Durations: {len(durations)} distinct"
          + (f"  ⚠ drift (> {MAX_DISTINCT_DURATIONS} — consolidate into tokens)"
             if report["duration_drift"] else ""))
    for k, v in list(report["durations"].items())[:12]:
        print(f"  {k:>10}  ×{v['count']:<4} e.g. {v['sample'][0]}")
    print(f"\nEasings: {len(easings)} distinct"
          + (f"  ⚠ drift (> {MAX_DISTINCT_EASINGS} off-token)" if report["easing_drift"] else ""))
    for k, v in report["easings"].items():
        if v["token"]:
            mark = "token"
        elif k.startswith("cubic-bezier"):
            mark = "off-token"
        elif k.startswith("const:"):
            mark = "unresolved-const"
        else:
            mark = "keyword"
        print(f"  ×{v['count']:<4} [{mark}] {k}  e.g. {v['sample'][0]}")
    if springs:
        print(f"\nSprings: {len(springs)} distinct config(s)")
        for k, v in report["springs"].items():
            print(f"  ×{v['count']:<4} {k}  e.g. {v['sample'][0]}")
    if exit_risk:
        print("\nExit-risk files (conditional <motion.*> mount, no AnimatePresence in file):")
        for f in exit_risk:
            print(f"  {f}")
    print("\nJudgment stays with the auditor: token-matching values and deliberate "
          "per-profile tempo differences are not findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
