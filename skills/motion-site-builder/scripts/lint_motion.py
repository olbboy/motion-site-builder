#!/usr/bin/env python3
"""
lint_motion — rule engine for motion UI/UX code (CSS / JSX / TSX / HTML).

Design contract:
- ALL taste (easings, ranges, whitelists, severities) comes from
  config/motion-tokens.json. Rules read config; they never hardcode values.
- Adding a rule = one function with the @rule decorator. Rules can be
  disabled or re-severitied from config["lint"] without touching code.

CLI:
    python3 lint_motion.py <file> [...files]              # lint files (cinematic profile)
    python3 lint_motion.py --profile product-ui <file>    # lint under another design profile
    python3 lint_motion.py --list-profiles                # list available design profiles
    python3 lint_motion.py --self-test                    # run built-in fixtures + profile checks

Profiles: cinematic (default, config/motion-tokens.json) + config/profiles/*.json.
Select via --profile <name> or the MOTION_PROFILE env var.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "..", "config", "motion-tokens.json")

ERROR, WARNING, INFO = "error", "warning", "info"


@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    suggestion: str
    line: int = 0


@dataclass
class Source:
    """Pre-parsed view of one code string so rules stay cheap and readable."""
    text: str
    path: str = "<inline>"
    lower: str = field(init=False)

    def __post_init__(self):
        self.lower = self.text.lower()

    def line_of(self, index: int) -> int:
        return self.text.count("\n", 0, index) + 1

    @property
    def has_video(self) -> bool:
        return "<video" in self.lower

    @property
    def has_animation(self) -> bool:
        """True when the source produces MOTION. Color/opacity-only transitions
        (transition-colors, transition-opacity) are excluded — reduced-motion
        targets movement, and non-moving fades are acceptable under it."""
        return bool(re.search(
            r"@keyframes|animation[-:]|transition-transform|transition-all"
            r"|transition\s*:\s*[^;}}\"']*(transform|all)"
            r"|motion\.|animate=|whileinview|whilehover|usescroll|requestanimationframe",
            self.lower))


PROFILES_DIR = os.path.join(SCRIPT_DIR, "..", "config", "profiles")


def resolve_profile_path(profile: str) -> str:
    """Map a profile name to its config file. cinematic/default/empty -> the
    root motion-tokens.json; a known profile -> config/profiles/<name>.json;
    anything unknown -> the default (callers can validate names separately)."""
    profile = (profile or "").strip().lower()
    if profile and profile not in ("cinematic", "default"):
        p = os.path.join(PROFILES_DIR, f"{profile}.json")
        if os.path.exists(p):
            return p
    return DEFAULT_CONFIG


def list_profiles() -> dict:
    """cinematic (root) + every config/profiles/*.json, name -> meta.note."""
    profiles = {"cinematic": "Video-first, glassmorphism, editorial serif, single-accent, dark — Apple-keynote energy (default)."}
    if os.path.isdir(PROFILES_DIR):
        for fn in sorted(os.listdir(PROFILES_DIR)):
            if fn.endswith(".json"):
                name = fn[:-5]
                try:
                    with open(os.path.join(PROFILES_DIR, fn), "r", encoding="utf-8") as f:
                        meta = json.load(f).get("meta", {})
                    profiles[name] = meta.get("note") or meta.get("name") or name
                except (OSError, json.JSONDecodeError):
                    profiles[name] = name
    return profiles


def load_config(path: str = None, profile: str = None) -> dict:
    with open(path or resolve_profile_path(profile), "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Rule registry ───────────────────────────────────────────────────

RULES = []  # list of (rule_id, default_severity, fn)


def rule(rule_id: str, severity: str):
    """Register a lint rule. fn(src: Source, cfg: dict) -> list[Finding-args]."""
    def decorator(fn):
        RULES.append((rule_id, severity, fn))
        return fn
    return decorator


def _norm_bezier(s: str) -> str:
    return re.sub(r"\s+", "", s.lower())


def _hex_to_hsl(hex_str: str):
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, l)
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hue = ((g - b) / d + (6 if g < b else 0)) / 6
    elif mx == g:
        hue = ((b - r) / d + 2) / 6
    else:
        hue = ((r - g) / d + 4) / 6
    return (hue * 360, s, l)


# ─── Rules M01–M12 ───────────────────────────────────────────────────

@rule("M01", ERROR)
def rule_reduced_motion(src: Source, cfg: dict):
    """Animated code must handle prefers-reduced-motion."""
    if src.path.endswith(".json"):  # manifests mention libs, they don't animate
        return []
    if not src.has_animation:
        return []
    if "prefers-reduced-motion" in src.lower or "usereducedmotion" in src.lower:
        return []
    return [dict(
        message="Animations present but no prefers-reduced-motion handling found.",
        suggestion="Add the reduced-motion boilerplate (catalog §11) or gate effects behind useReducedMotion()/matchMedia.",
    )]


@rule("M02", ERROR)
def rule_layout_prop_animation(src: Source, cfg: dict):
    """Only transform/opacity/filter may be animated."""
    findings = []
    # transition: <prop> or transition-property listing layout props
    for m in re.finditer(r"transition(?:-property)?\s*:\s*([^;}\"']+)", src.lower):
        props = m.group(1)
        bad = [p for p in ("width", "height", "top", "left", "right", "bottom", "margin", "padding")
               if re.search(rf"(^|[,\s]){p}\b", props)]
        if bad:
            findings.append(dict(
                message=f"Transition animates layout propert{'ies' if len(bad) > 1 else 'y'}: {', '.join(bad)}.",
                suggestion="Animate transform/opacity/filter instead (e.g. translate3d for movement).",
                line=src.line_of(m.start()),
            ))
    # @keyframes blocks touching layout props
    for m in re.finditer(r"@keyframes[^{]+\{((?:[^{}]*\{[^{}]*\})+)\s*\}", src.text, re.S):
        body = m.group(1).lower()
        bad = [p for p in ("width", "height", "top", "left", "margin", "padding")
               if re.search(rf"[{{;\s]{p}\s*:", body)]
        if bad:
            findings.append(dict(
                message=f"@keyframes animates layout properties: {', '.join(sorted(set(bad)))}.",
                suggestion="Use transform (translate/scale) and opacity in keyframes.",
                line=src.line_of(m.start()),
            ))
    return findings


@rule("M03", ERROR)
def rule_video_attrs(src: Source, cfg: dict):
    """Background <video> needs autoplay/muted/playsinline (+loop unless manual crossfade) and a poster."""
    if not src.has_video:
        return []
    findings = []
    required = [a.lower() for a in cfg.get("video", {}).get("required_attrs", [])]
    manual_loop = "timeupdate" in src.lower and ("ended" in src.lower or "crossfade" in src.lower)
    for m in re.finditer(r"<video\b[^>]*>", src.text, re.I | re.S):
        tag = m.group(0).lower().replace("-", "")
        missing = [a for a in required if a.replace("-", "") not in tag]
        if manual_loop and "loop" in missing:
            missing.remove("loop")  # crossfade loops manually
        if missing:
            findings.append(dict(
                message=f"<video> missing attribute(s): {', '.join(missing)}.",
                suggestion="Background video must be autoPlay muted playsInline (loop unless JS crossfade handles it).",
                line=src.line_of(m.start()),
            ))
        if cfg.get("video", {}).get("poster_required", True) and "poster" not in tag:
            findings.append(dict(
                severity=WARNING,
                message="<video> has no poster fallback.",
                suggestion="Add poster=\"...\" so slow connections and reduced-data users see a frame.",
                line=src.line_of(m.start()),
            ))
    return findings


@rule("M04", ERROR)
def rule_dependencies(src: Source, cfg: dict):
    """package.json only: dependencies must respect the whitelist."""
    if not src.path.endswith("package.json"):
        return []
    try:
        pkg = json.loads(src.text)
    except json.JSONDecodeError:
        return []
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    dep_cfg = cfg.get("dependencies", {})
    allowed = set(dep_cfg.get("allowed", []))
    forbidden = set(dep_cfg.get("forbidden", []))
    findings = []
    for name in deps:
        base = name  # scoped names compared whole
        if base in forbidden or any(base.startswith(f + "/") for f in forbidden):
            findings.append(dict(
                message=f"Forbidden dependency: {name}.",
                suggestion="Achieve the effect with the allowed stack (imagery + parallax, plain CSS).",
            ))
        elif allowed and base not in allowed and not base.startswith("@types/"):
            findings.append(dict(
                severity=WARNING,
                message=f"Dependency outside whitelist: {name}.",
                suggestion="Add it to config dependencies.allowed if intentional.",
            ))
    return findings


@rule("M05", WARNING)
def rule_accent_count(src: Source, cfg: dict):
    """At most N saturated accent hues (default 1)."""
    max_hues = cfg.get("palette", {}).get("max_accent_hues", 1)
    hues = []
    for m in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", src.text):
        hsl = _hex_to_hsl(m.group(0))
        if hsl and hsl[1] > 0.4 and 0.2 < hsl[2] < 0.8:
            hues.append(hsl[0])
    # cluster hues within 30° as one accent
    def hue_dist(a, b):
        d = abs(a - b) % 360
        return min(d, 360 - d)

    clusters = []
    for h in sorted(set(hues)):
        if all(hue_dist(h, c) > 30 for c in clusters):
            clusters.append(h)
    if len(clusters) > max_hues:
        distinct = len(clusters)
        return [dict(
            message=f"~{distinct} saturated accent hues detected (max {max_hues}).",
            suggestion="Keep ONE accent; express hierarchy with white opacity tiers.",
        )]
    return []


@rule("M06", WARNING)
def rule_entrance_timing(src: Source, cfg: dict):
    """Entrance durations within configured range; siblings staggered."""
    lo, hi = cfg.get("durations", {}).get("entrance", [0.5, 1.2])
    findings = []
    for m in re.finditer(r"animation\s*:\s*[\w-]+\s+([\d.]+)(m?s)([^;}\n]*)", src.lower):
        if "infinite" in m.group(3):
            continue  # looping animations (marquee, spin) are not entrances
        dur = float(m.group(1)) / (1000 if m.group(2) == "ms" else 1)
        if not lo <= dur <= hi:
            findings.append(dict(
                message=f"Entrance animation duration {dur}s outside [{lo}, {hi}]s.",
                suggestion="Keep entrances in the token range for the cinematic feel.",
                line=src.line_of(m.start()),
            ))
    # stagger heuristic: several .animate-* uses but no delay mechanism at all
    animated = len(re.findall(r"animate-fade|animate-\w+-up|initial=\{\{", src.lower))
    has_delay = bool(re.search(r"animation-delay|delay-\d|delay:\s*[\d.]", src.lower))
    if animated >= 3 and not has_delay:
        findings.append(dict(
            message=f"{animated} animated elements but no stagger delays found.",
            suggestion=f"Stagger siblings by {cfg.get('stagger', {}).get('default', 0.12)}s in narrative order.",
        ))
    return findings


@rule("M07", WARNING)
def rule_easing_tokens(src: Source, cfg: dict):
    """cubic-bezier values must come from the token set."""
    tokens = {_norm_bezier(v) for v in cfg.get("easings", {}).values() if "bezier" in v}
    findings = []
    for m in re.finditer(r"cubic-bezier\([^)]*\)", src.lower):
        if _norm_bezier(m.group(0)) not in tokens:
            findings.append(dict(
                message=f"Non-token easing: {m.group(0)}.",
                suggestion="Use an easing from config easings (expo-out for entrances, spring-pop for hovers) or add yours to the config.",
                line=src.line_of(m.start()),
            ))
    return findings


@rule("M08", WARNING)
def rule_decorative_noise(src: Source, cfg: dict):
    """No blobs/radial gradients competing with a video background."""
    if not src.has_video:
        return []
    findings = []
    # match CSS usage only — `radial-gradient(` or blob class names — not prose
    # like "no decorative blobs" in a prompt's CONSTRAINTS section
    for m in re.finditer(r"radial-gradient\s*\(|[.\-_]blob\b|\bblob[-_]", src.lower):
        findings.append(dict(
            message="Decorative radial-gradient/blob found alongside a video background.",
            suggestion="Remove it — the video provides all visual depth. (Contrast overlays bg-black/NN are fine.)",
            line=src.line_of(m.start()),
        ))
        break  # one finding per file is enough
    return findings


@rule("M09", WARNING)
def rule_layering(src: Source, cfg: dict):
    """Video background requires explicit z-index layering."""
    if not src.has_video:
        return []
    if re.search(r"z-\d|z-\[|z-index", src.lower):
        return []
    return [dict(
        message="Video background present but no explicit z-index layering.",
        suggestion="Declare layers: video z-0, overlay z-[1], content z-10, nav z-20.",
    )]


@rule("M10", WARNING)
def rule_transition_all(src: Source, cfg: dict):
    findings = []
    for m in re.finditer(r"transition\s*:\s*all\b|transition-all", src.lower):
        # skip negated prose mentions ("never transition: all") — common in prompt constraints
        prefix = src.lower[max(0, m.start() - 30):m.start()]
        if re.search(r"\b(never|no|avoid|not|don'?t)\b[^.;]*$", prefix):
            continue
        findings.append(dict(
            message="`transition: all` detected.",
            suggestion="List properties explicitly (transition-transform, transition-colors, transition-opacity).",
            line=src.line_of(m.start()),
        ))
    return findings


@rule("M11", INFO)
def rule_aria(src: Source, cfg: dict):
    """Markup with nav/buttons should carry some ARIA."""
    if not re.search(r"<nav\b|<button\b", src.lower):
        return []
    if "aria-" in src.lower:
        return []
    return [dict(
        message="Interactive markup without any ARIA attributes.",
        suggestion="Add aria-label to <nav> and icon-only buttons; aria-hidden on decorative video.",
    )]


@rule("M12", INFO)
def rule_display_tracking(src: Source, cfg: dict):
    """Huge display type should use negative tracking."""
    if cfg.get("typography", {}).get("display", {}).get("tracking") != "negative":
        return []
    has_display = re.search(r"text-(?:6|7|8|9)xl|font-size\s*:\s*(?:[6-9]\d|1\d\d)px", src.lower)
    if not has_display:
        return []
    if re.search(r"tracking-tight|tracking-\[-|letter-spacing\s*:\s*-", src.lower):
        return []
    return [dict(
        message="Display-size heading without negative tracking.",
        suggestion="Add tracking-tight or tracking-[-Npx] on display headings.",
    )]


# ─── Rules M13–M17 · interaction craft (Emil Kowalski doctrine) ──────
# These scope to INTERACTIVE elements (buttons/popovers/hover), never hero
# entrances — a marketing hero is first-time/rare and may run 0.5–1.2s.

@rule("M13", WARNING)
def rule_ease_in_ui(src: Source, cfg: dict):
    """`ease-in` on UI motion starts slow — it delays the exact moment the user
    watches most, so the interface feels sluggish."""
    if src.path.endswith(".json"):
        return []
    if not cfg.get("interaction", {}).get("ban_ease_in", True):
        return []
    findings = []
    # bare `ease-in` timing keyword (not ease-in-out / ease-out); also Framer "easeIn"
    for m in re.finditer(r"\bease-in\b(?!-out)|['\"]easein(?!out)['\"]", src.lower):
        prefix = src.lower[max(0, m.start() - 30):m.start()]
        if re.search(r"\b(never|no|avoid|not|don'?t)\b[^.;]*$", prefix):
            continue  # negated prose in prompt constraints ("never use ease-in")
        findings.append(dict(
            message="`ease-in` on UI motion — starts slow, feels sluggish.",
            suggestion="Use ease-out (or a strong custom curve) for entering/exiting; ease-in-out for on-screen moves.",
            line=src.line_of(m.start()),
        ))
    return findings


@rule("M14", WARNING)
def rule_scale_zero(src: Source, cfg: dict):
    """Never animate from scale(0) — nothing in the real world appears from
    nothing. Start from scale(0.9–0.97) + opacity."""
    if src.path.endswith(".json"):
        return []
    findings = []
    for m in re.finditer(r"scale3?d?\(\s*0\s*[,)]|scale\s*:\s*0\b(?!\.)", src.lower):
        findings.append(dict(
            message="Entrance animates from `scale(0)` — looks like it came from nowhere.",
            suggestion="Start from scale(0.9-0.97) + opacity: 0 instead.",
            line=src.line_of(m.start()),
        ))
    return findings


@rule("M15", INFO)
def rule_popover_origin(src: Source, cfg: dict):
    """Popovers/dropdowns/tooltips should scale from their trigger, not center.
    Modals are exempt — they stay centered."""
    if not cfg.get("interaction", {}).get("popover_origin_aware", True):
        return []
    if not re.search(r"popover|dropdown|tooltip", src.lower):
        return []
    has_scale = bool(re.search(r"scale\s*[(:]", src.lower))
    m = re.search(r"transform-origin\s*:\s*center", src.lower)
    if has_scale and m:
        return [dict(
            message="Popover/dropdown/tooltip uses transform-origin: center — should scale from its trigger.",
            suggestion="Use transform-origin: var(--radix-...-transform-origin) (Radix) or var(--transform-origin) (Base UI). Modals stay centered.",
            line=src.line_of(m.start()),
        )]
    return []


@rule("M16", INFO)
def rule_press_feedback(src: Source, cfg: dict):
    """Pressable elements should confirm the press with a subtle scale-down,
    so the UI feels like it's listening. An element that already animates on
    hover is button-like and should react to press too."""
    has_button = bool(re.search(r"<button\b|role=[\"']button[\"']", src.lower))
    hover_motion = bool(re.search(
        r"hover:(?:scale|-?translate|rotate)|:hover\s*\{[^}]*(?:transform|scale|translate)",
        src.lower))
    if not (has_button or hover_motion):
        return []
    if re.search(r":active|active:|whiletap|data-pressed", src.lower):
        return []
    subject = "Pressable element(s)" if has_button else "Element(s) with hover motion"
    return [dict(
        message=f"{subject} without press feedback.",
        suggestion="Add active:scale-[0.97] / :active { transform: scale(0.95-0.98) } (or Framer whileTap), ~160ms ease-out.",
    )]


@rule("M17", INFO)
def rule_hover_gate(src: Source, cfg: dict):
    """Raw-CSS :hover motion should be gated behind @media (hover: hover) —
    touch devices fire a false hover on tap. (Tailwind hover: utilities excluded.)"""
    if not cfg.get("interaction", {}).get("gate_hover_pointer_fine", True):
        return []
    moves = re.search(r":hover\s*\{[^}]*(transform|translate|scale)\b", src.lower)
    if not moves:
        return []
    if re.search(r"@media\s*\([^)]*hover\s*:\s*hover", src.lower):
        return []
    return [dict(
        message="Raw-CSS :hover motion not gated behind @media (hover: hover).",
        suggestion="Wrap hover transforms in @media (hover: hover) and (pointer: fine).",
        line=src.line_of(moves.start()),
    )]


# ─── Engine ──────────────────────────────────────────────────────────

def lint_source(src: Source, cfg: dict) -> list:
    lint_cfg = cfg.get("lint", {})
    disabled = set(lint_cfg.get("disabled_rules", []))
    overrides = lint_cfg.get("severity_overrides", {})
    findings = []
    for rule_id, default_sev, fn in RULES:
        if rule_id in disabled:
            continue
        for raw in fn(src, cfg):
            sev = raw.pop("severity", None) or overrides.get(rule_id, default_sev)
            findings.append(Finding(rule_id=rule_id, severity=sev, **raw))
    return findings


def score(findings: list, cfg: dict) -> dict:
    w = cfg.get("lint", {}).get("weights", {"error": 15, "warning": 5, "info": 1})
    counts = {s: sum(1 for f in findings if f.severity == s) for s in (ERROR, WARNING, INFO)}
    value = max(0, min(100, 100 - counts[ERROR] * w["error"] - counts[WARNING] * w["warning"] - counts[INFO] * w["info"]))
    grade = ("A+" if value >= 95 else "A" if value >= 90 else "B+" if value >= 85 else
             "B" if value >= 80 else "C" if value >= 70 else "D" if value >= 60 else "F")
    return {"score": value, "grade": grade,
            "summary": f"{counts[ERROR]} error(s), {counts[WARNING]} warning(s), {counts[INFO]} info(s)"}


def lint_code(code: str, path: str = "<inline>", cfg: dict = None, profile: str = None) -> dict:
    cfg = cfg or load_config(profile=profile)
    findings = lint_source(Source(code, path), cfg)
    return {"file": path, "findings": [asdict(f) for f in findings], **score(findings, cfg)}


def lint_file(path: str, cfg: dict = None, profile: str = None) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return lint_code(f.read(), path, cfg, profile)


# ─── Self-test fixtures ──────────────────────────────────────────────

BAD_FIXTURE = """
<video src="x.mp4"></video>
<div style="background: radial-gradient(circle, #ff0000, #00ff00)">
<h1 class="text-8xl">Hi</h1>
<button style="transition: all 0.3s ease-in">Go</button>
<div class="popover" style="transform-origin: center; transform: scale(0)"></div>
<style>@keyframes grow { from { width: 0; } to { width: 100px; } }
.x { animation: grow 2s; }
.pop { transition: transform 0.3s cubic-bezier(0.5, 0.2, 0.1, 1); }
.card:hover { transform: scale(1.2); }</style>
"""

GOOD_FIXTURE = """
<nav aria-label="Main"><button aria-label="Menu">≡</button></nav>
<video autoplay muted loop playsinline poster="p.jpg" class="z-0" aria-hidden="true"></video>
<div class="z-10">
<h1 class="text-8xl tracking-tight animate-fade-up">Hi</h1>
<p class="animate-fade-up delay-2">Sub</p>
<a class="animate-fade-up delay-3 transition-transform">CTA</a></div>
<style>
@keyframes fade-up { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
.animate-fade-up { animation: fade-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards; }
.animate-marquee { animation: marquee 40s linear infinite; }
button:active { transform: scale(0.97); transition: transform 160ms ease-out; }
@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; } }
</style>
"""


REQUIRED_CONFIG_KEYS = ("easings", "durations", "stagger", "typography", "palette",
                        "dependencies", "interaction", "lint")


def _check_profiles() -> dict:
    """Every profile must load, carry the required schema keys, and lint the
    fixtures without crashing. Keeps profiles from silently drifting."""
    results = {}
    ok = True
    for name in list_profiles():
        try:
            cfg = load_config(profile=name)
            missing_keys = [k for k in REQUIRED_CONFIG_KEYS if k not in cfg]
            # exercise the engine under this profile (must not raise)
            lint_code(GOOD_FIXTURE, "g.html", cfg)
            lint_code(BAD_FIXTURE, "b.html", cfg)
            results[name] = {"ok": not missing_keys, "missing_keys": missing_keys}
            ok = ok and not missing_keys
        except Exception as e:  # noqa: BLE001 — surface any profile that breaks the engine
            results[name] = {"ok": False, "error": str(e)}
            ok = False
    return {"ok": ok, "profiles": results}


def self_test() -> int:
    cfg = load_config()  # cinematic default
    bad = lint_code(BAD_FIXTURE, "bad.html", cfg)
    good = lint_code(GOOD_FIXTURE, "good.html", cfg)
    bad_rules = {f["rule_id"] for f in bad["findings"]}
    expected = {"M01", "M02", "M03", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12",
                "M13", "M14", "M15", "M16", "M17"}
    missing = expected - bad_rules
    profiles = _check_profiles()
    ok = not missing and good["score"] >= 90 and profiles["ok"]
    print(json.dumps({
        "bad_fixture": {"rules_fired": sorted(bad_rules), "missing_expected": sorted(missing), **{k: bad[k] for k in ("score", "grade")}},
        "good_fixture": {"rules_fired": sorted({f['rule_id'] for f in good['findings']}), **{k: good[k] for k in ("score", "grade")}},
        "profiles": profiles,
        "pass": ok,
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if args[0] == "--self-test":
        sys.exit(self_test())
    if args[0] == "--list-profiles":
        print(json.dumps(list_profiles(), indent=2, ensure_ascii=False))
        sys.exit(0)
    profile = os.environ.get("MOTION_PROFILE")
    if "--profile" in args:
        i = args.index("--profile")
        profile = args[i + 1] if i + 1 < len(args) else profile
        args = args[:i] + args[i + 2:]
    reports = [lint_file(p, profile=profile) for p in args]
    print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2, ensure_ascii=False))
    sys.exit(1 if any(f["severity"] == ERROR for r in reports for f in r["findings"]) else 0)
