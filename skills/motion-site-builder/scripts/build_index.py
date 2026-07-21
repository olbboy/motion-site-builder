#!/usr/bin/env python3
"""
build_index — scan a prompt library and generate data/prompt-index.json.

Extensibility contract: adding a new prompt .md to the library + re-running
this script is all it takes to make it retrievable via motion_find_reference.
Signals are regex heuristics — treat tags as "at least", not exhaustive.

CLI:
    python3 build_index.py [prompts_dir] [output_json]
Defaults: <repo>/prompts → ../data/prompt-index.json
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROMPTS = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "..", "prompts"))
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "..", "data", "prompt-index.json")

# technique signals: tag -> regex (case-insensitive)
TECHNIQUE_SIGNALS = {
    "video-bg": r"<video|video background|background video",
    "glass": r"liquid-glass|backdrop-blur|glassmorph",
    "framer-motion": r"framer[- ]motion|whileinview|usescroll|usetransform",
    "raf-lerp": r"\blerp\b|requestanimationframe",
    "crossfade-loop": r"crossfade|seamless loop",
    "sticky-stack": r"sticky.{0,40}(stack|card)|targetscale",
    "char-reveal": r"char(acter)?[- ]by[- ]char|per[- ]char|letter[- ]by[- ]letter",
    "marquee": r"marquee",
    "parallax": r"parallax",
    "magnetic-cursor": r"magnetic",
    "text-glow": r"text-glow|text-shadow: 0 0",
    "custom-easing": r"cubic-bezier",
    "fluid-type": r"clamp\(",
    "pill-ui": r"rounded-full",
    "reduced-motion": r"prefers-reduced-motion",
    "dark-theme": r"#0[0-9a-c]0|#000|bg-black|near-black|dark",
    "3d-imagery": r"\b3d\b",
    "iphone-frame": r"iphone|dynamic island",
}

FONT_PATTERN = re.compile(
    r"\b(Instrument Serif|Inter|Playfair Display|Geist|DM Sans|Kanit|Anton|Dancing Script|Space Grotesk|Manrope|Poppins|Bricolage Grotesque)\b")
HEX_PATTERN = re.compile(r"#[0-9a-fA-F]{6}\b")


def classify_archetype(rel_path: str, text: str, size: int) -> str:
    low = text.lower()
    if rel_path.startswith("apps/") or re.search(r"iphone|dynamic island", low):
        return "app-showcase"
    if re.search(r"styleguide|design system|style guide|replica", low):
        return "design-replica"
    if size > 8000 and re.search(r"section order|section \d|reusable components|footer", low):
        return "full-landing"
    # smaller specs still count as landings when they spec several distinct content sections
    section_signals = sum(1 for pat in (
        r"\bstats?\b", r"\bfeatures\b", r"\bpricing\b", r"testimonial", r"marquee",
        r"final cta", r"\bfooter\b", r"how it works", r"\bfaq\b",
    ) if re.search(pat, low))
    if section_signals >= 3:
        return "full-landing"
    return "minimal-hero"


def parse_readme_meta(prompts_dir: str) -> dict:
    """Map filename -> {name, category} from README markdown tables."""
    meta = {}
    readme = os.path.join(prompts_dir, "README.md")
    if not os.path.exists(readme):
        return meta
    with open(readme, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|", line)
            if m:
                meta[m.group(3).strip()] = {"name": m.group(1).strip(), "category": m.group(2).strip()}
    return meta


def index_prompt(prompts_dir: str, rel_path: str, meta: dict) -> dict:
    path = os.path.join(prompts_dir, rel_path)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    low = text.lower()

    techniques = sorted(tag for tag, pat in TECHNIQUE_SIGNALS.items() if re.search(pat, low))
    fonts = sorted(set(FONT_PATTERN.findall(text)))
    hexes = [h.lower() for h in HEX_PATTERN.findall(text)]
    stack = []
    for name, pat in (("react", r"\breact\b"), ("tailwind", r"tailwind"), ("typescript", r"typescript"),
                      ("vite", r"\bvite\b"), ("framer-motion", r"framer[- ]motion"),
                      ("lucide", r"lucide"), ("plain-html", r"single html file|plain html|vanilla js")):
        if re.search(pat, low):
            stack.append(name)

    entry_meta = meta.get(rel_path, {})
    return {
        "file": rel_path,
        "name": entry_meta.get("name") or os.path.splitext(os.path.basename(rel_path))[0].replace("-", " ").title(),
        "category": entry_meta.get("category", ""),
        "archetype": classify_archetype(rel_path, text, len(text)),
        "size_chars": len(text),
        "stack": stack,
        "fonts": fonts,
        "techniques": techniques,
        "palette_sample": sorted(set(hexes))[:8],
    }


def build(prompts_dir: str, output: str) -> dict:
    meta = parse_readme_meta(prompts_dir)
    entries = []
    for root, _dirs, files in os.walk(prompts_dir):
        for fname in sorted(files):
            if not fname.endswith(".md") or fname == "README.md":
                continue
            rel = os.path.relpath(os.path.join(root, fname), prompts_dir)
            entries.append(index_prompt(prompts_dir, rel, meta))

    index = {
        "meta": {
            # Keep generated output stable across local machines and CI. The
            # index only needs to identify the corpus, not record who built it.
            "source_dir": os.path.basename(os.path.abspath(prompts_dir)),
            "count": len(entries),
            "generator": "build_index.py",
            "note": "regex-derived tags are lower bounds; re-run after adding prompts",
        },
        "prompts": entries,
    }
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    return index


if __name__ == "__main__":
    prompts_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROMPTS
    output = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT
    if not os.path.isdir(prompts_dir):
        print(f"Prompts dir not found: {prompts_dir}", file=sys.stderr)
        sys.exit(1)
    index = build(prompts_dir, output)
    by_arch = {}
    for e in index["prompts"]:
        by_arch[e["archetype"]] = by_arch.get(e["archetype"], 0) + 1
    print(json.dumps({"indexed": index["meta"]["count"], "by_archetype": by_arch,
                      "output": os.path.abspath(output)}, indent=2))
