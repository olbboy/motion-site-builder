#!/usr/bin/env python3
"""
motion-site-tools — MCP server (stdio) for the motion-site-builder skill.

Zero external dependencies: a minimal JSON-RPC 2.0 stdio loop.
All taste comes from config/motion-tokens.json; the corpus index comes
from data/prompt-index.json (regenerate with build_index.py).

Tools:
    motion_list_profiles   list design profiles (cinematic default + others)
    motion_validate        lint a code string (CSS/JSX/TSX/HTML)
    motion_validate_file   lint a file on disk
    motion_get_tokens      full design tokens JSON (per profile)
    motion_get_template    verbatim snippet from the component catalog
    motion_suggest_pattern motion pattern for an intent
    motion_easing_rationale easing + duration + why for a motion intent
    motion_find_reference  nearest corpus prompts by query/archetype

MCP config:
    { "mcpServers": { "motion-site-tools": {
        "command": "python3", "args": ["<path>/scripts/server.py"] } } }
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))

sys.path.insert(0, SCRIPT_DIR)
import lint_motion  # noqa: E402


# ─── Data loading ────────────────────────────────────────────────────

def _config(profile: str = None) -> dict:
    return lint_motion.load_config(profile=profile)


def _index() -> dict:
    path = os.path.join(SKILL_ROOT, "data", "prompt-index.json")
    if not os.path.exists(path):
        return {"meta": {"count": 0}, "prompts": [],
                "error": "prompt-index.json not found — run scripts/build_index.py"}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _catalog_section(name: str) -> str:
    """Extract one `## N. name` section from the component catalog."""
    path = os.path.join(SKILL_ROOT, "references", "component-catalog.md")
    with open(path, "r", encoding="utf-8") as f:
        catalog = f.read()
    sections = re.findall(r"^## \d+\.\s*(\S+)", catalog, re.M)
    m = re.search(rf"^## \d+\.\s*{re.escape(name)}\s*$(.*?)(?=^## \d+\.|\Z)", catalog, re.M | re.S)
    if not m:
        return json.dumps({"error": f"Unknown template: {name}", "valid_templates": sections})
    return f"## {name}{m.group(1).rstrip()}"


# ─── Pattern knowledge base (per profile; values from config) ────────

PROFILE_NAMES = ("cinematic", "product-ui", "editorial", "playful", "ecommerce")


def _interaction_patterns(cfg: dict) -> dict:
    """Universal interaction patterns — apply to EVERY profile."""
    ease = cfg.get("easings", {})
    return {
        "press": {
            "recommended": "Press feedback on every pressable element: active:scale-[0.95-0.98] (or Framer "
                           "whileTap), quick ease-out. See interaction-standards.md §4.",
            "template": "press-scale-button",
            "avoid": "No :active/whileTap state; scale(0); durations over the press range",
        },
        "hover": {
            "recommended": "Subtle hover: scale(1.02-1.05) or a small translateY lift, gated behind "
                           "@media (hover: hover); always paired with press feedback.",
            "template": "press-scale-button",
            "avoid": "Ungated :hover motion (touch fires it on tap); color-only hover; scale beyond ~1.1",
        },
        "popover": {
            "recommended": "Scale from the trigger, not center: transform-origin: var(--radix-...-transform-origin) "
                           "(Radix) or var(--transform-origin) (Base UI). 150-250ms ease-out. Modals stay centered.",
            "template": "origin-aware-popover",
            "avoid": "transform-origin: center on a trigger-anchored popover; scale(0); ease-in",
        },
        "toast": {
            "recommended": "Interruptible: CSS transition (retargets mid-flight) + @starting-style, not @keyframes. "
                           "translateY(100%) hides by own height. Spring for swipe-to-dismiss.",
            "template": "interruptible-toast",
            "avoid": "@keyframes on rapidly-added toasts (restart from zero); hardcoded px offsets",
        },
    }


def _macro_patterns(cfg: dict, profile: str) -> dict:
    """Composition-level patterns that vary by design profile."""
    ease = cfg.get("easings", {})
    dur = cfg.get("durations", {})
    stag = cfg.get("stagger", {})
    ent = dur.get("entrance", [0.5, 1.2])
    st = stag.get("default", 0.12)
    reveal = dur.get("scroll_reveal", [0.5, 1.0])
    strong = ease.get("expo-out") or ease.get("quint-out") or ease.get("ease-out", "ease-out")
    sets = {
        "cinematic": {
            "entrance": {"recommended": f"Staggered fade-rise: translateY 16-32px -> 0, {ent}s, stagger {st}s, {strong}",
                         "template": "entrance-keyframes", "avoid": "Everything at once; durations over the entrance range"},
            "ambient_depth": {"recommended": "Fullscreen looping video + explicit z-layers (video z-0, overlay z-[1], content z-10, nav z-20)",
                              "template": "video-background", "avoid": "WebGL/Three.js, decorative blobs, radial gradients"},
            "seamless_loop": {"recommended": f"JS crossfade near clip end (rAF, {dur.get('video_crossfade', [0.4, 0.7])}s fade, guard flag)",
                              "template": "video-crossfade-loop", "avoid": "CSS transition on <video>; visible restart jump"},
            "scroll_story": {"recommended": "Framer useScroll + useTransform for parallax; whileInView once:true for reveals",
                             "template": "scroll-char-reveal", "avoid": "Scroll-jacking; mixing two scroll libraries"},
            "parallax": {"recommended": "Hand-rolled rAF + lerp (current += (target-current)*0.08..0.12) on translate3d",
                         "template": "raf-lerp-parallax", "avoid": "Animating top/left; missing reduced-motion gate"},
            "section_stacking": {"recommended": "Sticky-stack cards: scale = 1 - (n-1-i)*0.03, sticky top offsets",
                                 "template": "sticky-stack-cards", "avoid": "Carousel plugins"},
            "text_drama": {"recommended": "Char-by-char opacity 0.2 -> 1 mapped to scroll progress",
                           "template": "scroll-char-reveal", "avoid": "Typewriter with blinking cursor"},
            "navigation": {"recommended": "liquid-glass rounded-full pill, z-20, links text-white/80 hover:text-white",
                           "template": "glass-nav-pill", "avoid": "Opaque navbars over video; hamburger on desktop"},
        },
        "product-ui": {
            "entrance": {"recommended": f"Fast list/card entrance: fade + translateY 4-12px, {ent}s, stagger {st}s, {strong}. The UI appears, it doesn't perform.",
                         "template": "product-ui-stat-card", "avoid": "Cinematic 0.8s reveals; blur; large travel"},
            "list_stagger": {"recommended": f"Row-by-row stagger on table/list mount, ~{st}s apart, same fast ease-out",
                             "template": "product-ui-data-row", "avoid": "Everything at once; long delays that stall data"},
            "panel_slide": {"recommended": "Drawer/sheet/side-panel: interruptible CSS transition + @starting-style, translateX/Y(100%)",
                            "template": "interruptible-toast", "avoid": "@keyframes that restart; animating width"},
            "skeleton_load": {"recommended": "Shimmer skeleton (linear sweep) while data loads, then crossfade to content",
                              "avoid": "Layout jump when data arrives; a spinner where a skeleton belongs"},
            "navigation": {"recommended": "Persistent sidebar / top bar; active item via color + a moving indicator (layout animation), no page-level motion",
                           "avoid": "Animating the nav on every route; glass pills over nothing"},
        },
        "editorial": {
            "reading_flow": {"recommended": "Prose column max-w-[65ch], generous leading; content just reads — motion stays out of the way",
                             "template": "editorial-prose", "avoid": "Motion competing with reading; autoplaying anything"},
            "scroll_reveal": {"recommended": f"Gentle fade+rise as sections enter the viewport, {reveal}s, fired once",
                              "avoid": "Parallax that fights scroll; re-triggering on every pass"},
            "sticky_toc": {"recommended": "Sticky table-of-contents highlighting the active heading (IntersectionObserver); smooth-scroll on click",
                           "template": "editorial-sticky-toc", "avoid": "Scroll-jacking; jumpy active states"},
            "reading_progress": {"recommended": "Thin top progress bar bound to scroll via transform: scaleX (GPU-only)",
                                 "avoid": "Animating width; heavy JS on every scroll event"},
            "image_reveal": {"recommended": "Figures reveal with clip-path inset on enter; captions fade in just after",
                             "avoid": "Big zoom/parallax on every image"},
        },
        "playful": {
            "pop_entrance": {"recommended": f"Pop-in with overshoot (spring / back-out), {ent}s; visible bounce is welcome here",
                             "template": "playful-pop-cta", "avoid": "Flat linear entrances; timid scale"},
            "sticker_hover": {"recommended": "Chunky hover: scale(1.05-1.08) + slight rotate, spring; gated behind @media (hover: hover)",
                              "template": "playful-sticker-badge", "avoid": "Ungated hover; scale that clips neighbors"},
            "marquee": {"recommended": "Bold scrolling marquee (CSS loop, linear) used as a design element",
                        "avoid": "ease-* on the loop; visible restart jump"},
            "decor_motion": {"recommended": "Floating decorative shapes/gradients (transform translate/rotate loop) — the identity here; keep GPU-only + reduced-motion-gated",
                             "avoid": "Animating layout; ignoring reduced-motion"},
            "navigation": {"recommended": "Chunky rounded/pill nav with a bouncy active state; color-forward",
                           "avoid": "Muted glass; tiny tap targets"},
        },
        "ecommerce": {
            "product_grid": {"recommended": f"Card grid fade+rise into place, {ent}s, small stagger {st}s; snappy so browsing feels fast",
                             "template": "ecommerce-product-card", "avoid": "Slow cinematic reveals; layout shift as images load"},
            "product_hover": {"recommended": "Card hover: crossfade to the alt product shot + subtle lift (translateY), gated for touch",
                              "template": "ecommerce-product-card", "avoid": "Ungated hover; a zoom that reflows the grid"},
            "quick_view": {"recommended": "Quick-view modal: origin-aware scale-in from the card, interruptible, with a dim scrim",
                           "template": "origin-aware-popover", "avoid": "Full-page nav for a peek; scale(0)"},
            "add_to_cart": {"recommended": "Add-to-cart press feedback + a badge-count bump (or fly-to-cart); crisp confirmation",
                            "template": "ecommerce-add-to-cart", "avoid": "No feedback on add; slow confirmation"},
            "navigation": {"recommended": "Sticky header + interruptible cart drawer; optional announcement bar",
                           "avoid": "Hiding the cart; janky sticky behavior"},
        },
    }
    return sets.get(profile, sets["cinematic"])


def _pattern_matrix(cfg: dict, profile: str = None) -> dict:
    profile = (profile or "cinematic").strip().lower()
    if profile not in PROFILE_NAMES:
        profile = "cinematic"
    return {**_macro_patterns(cfg, profile), **_interaction_patterns(cfg)}


# ─── Easing decision framework (structure fixed, values from config) ─
# The "which easing, how fast, and why" framework, made programmatic and
# profile-aware. Curves resolve by KIND from whatever the active profile
# defines (never hardcoded), so it stays correct across design languages.
# Reveal-tier intents (entrance/scroll) keep that profile's long budget;
# interaction-tier intents obey its sub-<ui_max> bar.

def _easing_guide(cfg: dict) -> dict:
    ease = cfg.get("easings", {})
    dur = cfg.get("durations", {})
    inter = cfg.get("interaction", {})
    press = inter.get("press_duration_ms", [100, 160])
    ui_max = inter.get("ui_max_duration_ms", 300)
    entrance = dur.get("entrance", [0.5, 1.2])
    reveal = dur.get("scroll_reveal", [0.5, 1.0])

    def pick(*names):
        """Resolve a curve by kind from the profile's easings, in preference
        order; fall back to the first bezier defined, then a bare keyword."""
        for n in names:
            if n in ease:
                return {"token": n, "value": ease[n]}
        for k, v in ease.items():
            if "bezier" in str(v):
                return {"token": k, "value": v}
        return {"token": names[-1] if names else "ease-out", "value": names[-1] if names else "ease-out"}

    strong_out = pick("expo-out", "quint-out", "ease-out")   # reveals / entrances
    ui_out = pick("ease-out", "expo-out", "quint-out")        # interaction feedback
    inout = pick("ease-in-out", "standard")                  # on-screen moves
    springy = pick("spring-pop", "back-out")                 # playful pops
    hover_val = f"{ui_out['value']} (or {springy['value']} for a playful pop)"
    return {
        "entrance": {
            "layer": "reveal",
            "easing": strong_out,
            "duration": f"{entrance[0]}-{entrance[1]}s (reveal tier — exempt from the <{ui_max}ms interaction rule)",
            "why": "Entering elements use ease-out: it starts fast, so the moment the user watches most gets immediate movement. Use this profile's strongest ease-out curve.",
            "avoid": "ease-in (delays the start); scale(0) (nothing appears from nothing).",
        },
        "exit": {
            "layer": "interaction",
            "easing": ui_out,
            "duration": f"120-{ui_max}ms (snappy — the system is responding)",
            "why": "Exits use ease-out and stay quick: the system is responding, not deciding. Enter can be slower than exit (asymmetric timing).",
            "avoid": "ease-in; symmetric enter/exit timing on a press-and-release.",
        },
        "move": {
            "layer": "interaction",
            "easing": inout,
            "duration": f"150-{ui_max}ms",
            "why": "Elements already on screen moving from A to B use ease-in-out — natural acceleration and deceleration.",
            "avoid": "ease-out on a pure reposition (abrupt start); animating top/left instead of transform.",
        },
        "hover": {
            "layer": "interaction",
            "easing": {"token": f"{ui_out['token']} / {springy['token']}", "value": hover_val},
            "duration": f"{press[0]}-{press[1]}ms",
            "why": "Hover/color changes use a gentle ease; a scale pop can use the spring curve. Pair with press feedback and gate raw-CSS hover behind @media (hover: hover).",
            "avoid": "scale beyond ~1.1; ungated :hover motion on touch.",
        },
        "press": {
            "layer": "interaction",
            "easing": ui_out,
            "duration": f"{press[0]}-{press[1]}ms",
            "why": "Press feedback (transform: scale(0.95-0.98)) uses a quick ease-out so the tap feels instantly acknowledged.",
            "avoid": "ease-in; scale(0); durations over the press range.",
        },
        "popover": {
            "layer": "interaction",
            "easing": strong_out,
            "duration": f"150-250ms (< {ui_max}ms)",
            "why": "Popovers/dropdowns/tooltips scale in from their trigger with a strong ease-out; keep them fast so they feel instant.",
            "avoid": "ease-in; transform-origin: center (scale from the trigger). Modals are exempt (centered).",
        },
        "toast": {
            "layer": "interaction",
            "easing": {"token": strong_out["token"], "value": f"{strong_out['value']} (or an iOS-like drawer curve cubic-bezier(0.32, 0.72, 0, 1))"},
            "duration": "200-500ms",
            "why": "Toasts/drawers use ease-out and MUST be interruptible — CSS transition + @starting-style (or a spring), never @keyframes that restart from zero.",
            "avoid": "@keyframes on rapidly-added toasts; ease-in; hardcoded px offsets (use translateY(100%)).",
        },
        "constant": {
            "layer": "ambient",
            "easing": {"token": "linear", "value": "linear"},
            "duration": "loop duration (e.g. marquee 40s, spinner 1s)",
            "why": "Continuous motion (marquee, spinner, progress) uses linear — any easing makes a loop stutter at the seam.",
            "avoid": "ease-* on loops; visible restart jump.",
        },
        "scroll_reveal": {
            "layer": "reveal",
            "easing": strong_out,
            "duration": f"{reveal[0]}-{reveal[1]}s",
            "why": "Scroll-triggered reveals use a strong ease-out, fired once (whileInView once:true) so they don't replay on every scroll.",
            "avoid": "ease-in; replaying the reveal on each scroll pass.",
        },
    }


_EASING_KEYWORDS = {
    "entrance": ["enter", "appear", "reveal on load", "intro", "hero", "load", "hiện", "vào"],
    "exit": ["exit", "leave", "dismiss", "close", "out", "thoát", "đóng"],
    "move": ["move", "reposition", "morph", "shift", "between", "slide between"],
    "hover": ["hover", "cursor"],
    "press": ["press", "tap", "click", "active", "button", "cta", "nhấn", "bấm"],
    "popover": ["popover", "dropdown", "tooltip", "menu", "select"],
    "toast": ["toast", "drawer", "sheet", "snackbar", "notification", "thông báo"],
    "constant": ["marquee", "spinner", "progress", "loop", "linear", "ambient", "lặp"],
    "scroll_reveal": ["scroll", "inview", "reveal on scroll", "parallax", "cuộn"],
}


# ─── Minimal MCP stdio server ────────────────────────────────────────

class MCPServer:
    def __init__(self, name: str):
        self.name = name
        self._tools = {}
        self._handlers = {}

    def tool(self, description: str, params: dict, required: list):
        def decorator(fn):
            self._tools[fn.__name__] = {
                "name": fn.__name__,
                "description": description,
                "inputSchema": {"type": "object", "properties": params, "required": required},
            }
            self._handlers[fn.__name__] = fn
            return fn
        return decorator

    def _reply(self, msg_id, result):
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    def handle(self, msg: dict):
        method, msg_id = msg.get("method", ""), msg.get("id")
        if method == "initialize":
            return self._reply(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": self.name, "version": "1.0.0"},
            })
        if method == "tools/list":
            return self._reply(msg_id, {"tools": list(self._tools.values())})
        if method == "tools/call":
            params = msg.get("params", {})
            fn = self._handlers.get(params.get("name", ""))
            if not fn:
                return self._reply(msg_id, {
                    "content": [{"type": "text", "text": f"Unknown tool: {params.get('name')}"}],
                    "isError": True})
            try:
                result = fn(**params.get("arguments", {}))
                text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2)
                return self._reply(msg_id, {"content": [{"type": "text", "text": text}]})
            except Exception as e:  # surface tool errors to the client, keep server alive
                return self._reply(msg_id, {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True})
        if msg_id is not None:  # unknown request → empty result keeps clients happy
            return self._reply(msg_id, {})
        return None  # notification

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            resp = self.handle(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()


mcp = MCPServer("motion-site-tools")


# ─── Tools ───────────────────────────────────────────────────────────

@mcp.tool(
    "Lint a code string (CSS/JSX/TSX/HTML) against the motion design rules. "
    "Returns findings (error/warning/info), score 0-100 and grade. "
    "Call after writing each file. Pass file_name='package.json' to check dependencies. "
    "Pass profile to lint under a design language other than cinematic (see motion_list_profiles).",
    {"code": {"type": "string"}, "file_name": {"type": "string", "default": "<inline>"},
     "profile": {"type": "string", "default": ""}},
    ["code"])
def motion_validate(code: str, file_name: str = "<inline>", profile: str = ""):
    return lint_motion.lint_code(code, file_name, profile=profile or None)


@mcp.tool(
    "Lint a file on disk against the motion design rules (same output as motion_validate). "
    "Pass profile for a non-cinematic design language.",
    {"file_path": {"type": "string"}, "profile": {"type": "string", "default": ""}},
    ["file_path"])
def motion_validate_file(file_path: str, profile: str = ""):
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    return lint_motion.lint_file(file_path, profile=profile or None)


@mcp.tool(
    "Get the full design tokens (easings, durations, stagger, typography, palette families, "
    "layering, dependency whitelist, video rules) for a design profile. Default is cinematic "
    "(config/motion-tokens.json); pass profile=product-ui|editorial|playful|ecommerce for another.",
    {"profile": {"type": "string", "default": ""}}, [])
def motion_get_tokens(profile: str = ""):
    return _config(profile or None)


@mcp.tool(
    "List the available design profiles (cinematic default + others) with a one-line description "
    "of each. Pick one FIRST, then pass its name as the `profile` arg to the other tools.",
    {}, [])
def motion_list_profiles():
    return {"default": "cinematic", "profiles": lint_motion.list_profiles(),
            "usage": "Pass profile='<name>' to motion_get_tokens / motion_validate / motion_suggest_pattern "
                     "/ motion_easing_rationale, or set MOTION_PROFILE for the CLI."}


@mcp.tool(
    "Get a verbatim code snippet from the component catalog. Cinematic + universal: liquid-glass, "
    "text-glow, entrance-keyframes, video-background, video-crossfade-loop, glass-nav-pill, "
    "hero-block, raf-lerp-parallax, sticky-stack-cards, scroll-char-reveal, "
    "reduced-motion-boilerplate, iphone-frame, press-scale-button, origin-aware-popover, "
    "interruptible-toast, hold-to-confirm. Profile primitives: product-ui-stat-card, "
    "product-ui-data-row, editorial-prose, editorial-sticky-toc, playful-pop-cta, "
    "playful-sticker-badge, ecommerce-product-card, ecommerce-add-to-cart.",
    {"name": {"type": "string"}}, ["name"])
def motion_get_template(name: str):
    return _catalog_section(name.strip().lower())


@mcp.tool(
    "Suggest a motion pattern for an intent. Intents are PER PROFILE plus universal interaction "
    "(press, hover, popover, toast). Cinematic: entrance, ambient_depth, seamless_loop, scroll_story, "
    "parallax, section_stacking, text_drama, navigation. product-ui: entrance, list_stagger, panel_slide, "
    "skeleton_load, navigation. editorial: reading_flow, scroll_reveal, sticky_toc, reading_progress, "
    "image_reveal. playful: pop_entrance, sticker_hover, marquee, decor_motion, navigation. ecommerce: "
    "product_grid, product_hover, quick_view, add_to_cart, navigation. Free-text is fuzzy-matched; "
    "pass profile to get that profile's patterns and tokens.",
    {"intent": {"type": "string"}, "context": {"type": "string", "default": ""},
     "profile": {"type": "string", "default": ""}},
    ["intent"])
def motion_suggest_pattern(intent: str, context: str = "", profile: str = ""):
    matrix = _pattern_matrix(_config(profile or None), profile or None)
    key = intent.lower().strip().replace(" ", "_").replace("-", "_")
    if key not in matrix:
        # broad keyword map (union across profiles); only match intents present
        # in the ACTIVE profile's matrix
        keywords = {
            "entrance": ["intro", "appear", "load", "first", "reveal on load", "hiện", "vào"],
            "ambient_depth": ["background", "depth", "video", "atmosphere", "nền"],
            "seamless_loop": ["seamless", "video loop", "restart"],
            "scroll_story": ["scroll story", "storytelling"],
            "parallax": ["parallax", "lerp", "mượt"],
            "section_stacking": ["stack", "sticky cards", "chồng"],
            "text_drama": ["char", "letter", "chữ", "text reveal"],
            "list_stagger": ["list", "table", "rows", "grid mount", "danh sách", "bảng"],
            "panel_slide": ["drawer", "sheet", "side panel", "slide in panel"],
            "skeleton_load": ["skeleton", "shimmer", "loading", "placeholder"],
            "reading_flow": ["prose", "article", "reading", "long-form", "bài viết"],
            "scroll_reveal": ["scroll reveal", "inview", "cuộn hiện", "on scroll"],
            "sticky_toc": ["toc", "table of contents", "outline", "mục lục"],
            "reading_progress": ["progress bar", "reading progress", "scroll progress"],
            "image_reveal": ["image reveal", "figure", "clip-path", "photo reveal"],
            "pop_entrance": ["pop", "bounce", "overshoot", "springy"],
            "sticker_hover": ["sticker", "chunky hover", "wobble", "rotate hover"],
            "marquee": ["marquee", "ticker strip", "scrolling text", "băng chạy"],
            "decor_motion": ["blob", "floating shapes", "decor", "gradient move"],
            "product_grid": ["product grid", "catalog", "shop grid", "lưới sản phẩm"],
            "product_hover": ["product hover", "image swap", "alt shot", "card lift"],
            "quick_view": ["quick view", "quick-view", "peek", "xem nhanh"],
            "add_to_cart": ["add to cart", "cart", "buy", "giỏ hàng", "thêm giỏ"],
            "hover": ["hover", "cursor"],
            "press": ["press", "button", "tap", "active", "click", "cta", "nhấn", "bấm"],
            "popover": ["popover", "dropdown", "tooltip", "menu open", "select"],
            "toast": ["toast", "snackbar", "notification", "thông báo"],
            "navigation": ["nav", "menu", "header", "sidebar", "điều hướng"],
        }
        # include the raw intent (spaces intact) so multi-word keywords match
        combined = f"{intent} {key} {context}".lower()
        key = next((k for k, kws in keywords.items()
                    if k in matrix and any(kw in combined for kw in kws)), None)
    if not key:
        return {"error": f"Unknown intent: {intent}", "profile": profile or "cinematic",
                "valid_intents": list(matrix.keys())}
    out = {"intent": key, "profile": profile or "cinematic", **matrix[key]}
    if matrix[key].get("template"):
        out["next_step"] = f"Call motion_get_template('{matrix[key]['template']}') for the verbatim snippet."
    return out


@mcp.tool(
    "Get the right easing curve + duration + rationale for a motion intent (the easing "
    "decision framework, made programmatic and config-driven). Valid intents: entrance, exit, "
    "move, hover, press, popover, toast, constant, scroll_reveal. Free-text is fuzzy-matched. "
    "Cinematic intents (entrance/scroll_reveal) keep the long budget; interaction intents obey "
    "the sub-300ms bar. Use motion_suggest_pattern for the full pattern; motion_get_tokens for raw values. "
    "Pass profile for non-cinematic easing/duration budgets.",
    {"intent": {"type": "string"}, "element": {"type": "string", "default": ""},
     "profile": {"type": "string", "default": ""}},
    ["intent"])
def motion_easing_rationale(intent: str, element: str = "", profile: str = ""):
    cfg = _config(profile or None)
    guide = _easing_guide(cfg)
    key = intent.lower().strip().replace(" ", "_").replace("-", "_")
    if key not in guide:
        combined = f"{key} {element}".lower()
        key = next((k for k, kws in _EASING_KEYWORDS.items()
                    if any(kw in combined for kw in kws)), None)
    if not key:
        return {"error": f"Unknown intent: {intent}", "valid_intents": list(guide.keys())}
    out = {"intent": key, **guide[key],
           "reference": "interaction-standards.md §2-§3; motion-design-dna.md §6"}
    if out["layer"] != "ambient" and cfg.get("interaction", {}).get("ban_ease_in", True):
        out["rule"] = "Never use ease-in on interactive UI — it delays the exact moment the user is watching."
    return out


@mcp.tool(
    "Find the closest reference prompts in the corpus. Query is matched against name, "
    "category, techniques, fonts and stack; optionally filter by archetype "
    "(minimal-hero | full-landing | design-replica | app-showcase). "
    "Adapt the top hit instead of generating from scratch.",
    {"query": {"type": "string"},
     "archetype": {"type": "string", "default": ""},
     "limit": {"type": "integer", "default": 3}},
    ["query"])
def motion_find_reference(query: str, archetype: str = "", limit: int = 3):
    idx = _index()
    if "error" in idx:
        return idx
    terms = [t for t in re.split(r"[,\s/]+", query.lower()) if len(t) > 2]
    scored = []
    for e in idx["prompts"]:
        if archetype and e["archetype"] != archetype:
            continue
        haystacks = {
            "name": e["name"].lower(), "category": e["category"].lower(),
            "techniques": " ".join(e["techniques"]),
            "fonts": " ".join(e["fonts"]).lower(), "stack": " ".join(e["stack"]),
            "file": e["file"].lower(),
        }
        s = 0
        for t in terms:
            if t in haystacks["name"] or t in haystacks["file"]:
                s += 3
            if t in haystacks["category"]:
                s += 2
            if t in haystacks["techniques"] or t in haystacks["stack"] or t in haystacks["fonts"]:
                s += 1
        if s > 0 or (archetype and not terms):
            scored.append((s, e))
    scored.sort(key=lambda x: (-x[0], x[1]["file"]))
    hits = [{"match_score": s, **e} for s, e in scored[:max(1, limit)]]
    return {"query": query, "archetype_filter": archetype or "(none)",
            "hits": hits,
            "source_dir": idx["meta"].get("source_dir", ""),
            "tip": "Read the top hit's file and adapt values (brand, copy, accent, video URL)."}


if __name__ == "__main__":
    mcp.run()
