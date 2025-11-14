# structure.py
# Reusable narration panel + scripted scene engine (Manim CE v0.19)

from manim import *
import numpy as np

# ---------- DEFAULT THEME ----------
DEFAULT_THEME = {
    "subject": "Your Subject",
    "font": None,                # None -> use Manim's default; set a name in your SCRIPT to override
    "text_color": WHITE,
    "accent_color": YELLOW_A,
    "panel_bg": GREY_E,
    "panel_opacity": 1.0,
    "panel_corner_radius": 0.15,  # kept for optional rounding (off by default)
    "panel_padding": 0.35,
    "panel_height": 2.5,
    "panel_margins": 0.1,
    "title_size": 36,
    "step_size": 28,
    "body_size": 26,
    "line_spacing": 0.24,
    "max_body_width_ratio": 0.94,
    "progress_style": "dots",     # "dots" | "bar" | None
    "progress_color": "#b5b5b5",
    "progress_active_color": "#ffffff",
    "progress_bar_height": 0.12,
    "progress_bar_padding": 0.18,
    "default_hold": 1.0,
    "transition_time": 0.5,
    "appear_time": 0.6,
    "rounded": False,             # set True to try rounded corners (guarded)
}

# ---------- small geometry helpers (avoid [] indexing completely) ----------
def left_x(mobj: Mobject) -> float:
    return float(mobj.get_x() - mobj.width / 2)

def right_x(mobj: Mobject) -> float:
    return float(mobj.get_x() + mobj.width / 2)

def top_y(mobj: Mobject) -> float:
    return float(mobj.get_y() + mobj.height / 2)

def bottom_y(mobj: Mobject) -> float:
    return float(mobj.get_y() - mobj.height / 2)

# ---------- safe text builders ----------
def _make_text(s: str, t: dict, scale: float):
    kwargs = {"color": t["text_color"]}
    if t.get("font"):
        kwargs["font"] = t["font"]
    return Text(s, **kwargs).scale(scale)

def _make_paragraph(lines, t: dict, scale: float):
    kwargs = {
        "alignment": "left",                 # string, not vector
        "line_spacing": t["line_spacing"],
        "color": t["text_color"],
    }
    if t.get("font"):
        kwargs["font"] = t["font"]
    return Paragraph(*lines, **kwargs).scale(scale)

# ---------- PANEL ----------
class StepPanel(VGroup):
    def __init__(self, frame, theme, total_steps=0, **kwargs):
        super().__init__(**kwargs)
        self.frame = frame
        self.theme = theme
        self.total_steps = total_steps

        t = self.theme
        self.width = frame.width - 2 * t["panel_margins"]
        self.inner_width = self.width - 2 * t["panel_padding"]

        # Rectangle panel (optional rounding guarded)
        self.bg = Rectangle(
            width=self.width,
            height=t["panel_height"],
            fill_color=t["panel_bg"],
            fill_opacity=t["panel_opacity"],
            stroke_opacity=0,
        )
        if t.get("rounded"):
            try:
                self.bg.round_corners(float(t["panel_corner_radius"]))
            except Exception as e:
                print(f"[WARN] round_corners disabled due to: {e}")

        # Subject & headline
        self.subject = _make_text(t["subject"], t, t["title_size"] / 48)
        self.step_headline = _make_text("", t, t["step_size"] / 48)

        # Body paragraph (start empty)
        self.body = _make_paragraph([""], t, t["body_size"] / 24)

        # Progress
        self.progress_group = VGroup()
        self._rebuild_progress()

        # Layout + dock
        self._layout_inside()
        self.move_to(self._bottom_anchor())
        self.add(self.bg, self.subject, self.step_headline, self.body, self.progress_group)

    # --- layout helpers ---
    def _bottom_anchor(self):
        t = self.theme
        y = bottom_y(self.frame) + t["panel_margins"] + t["panel_height"] / 2
        return np.array([0.0, float(y), 0.0])  # ensure 3 floats

    def _rebuild_progress(self):
        t = self.theme
        self.progress_group = VGroup()
        style = t["progress_style"]
        if not style or self.total_steps <= 1:
            return
        if style == "dots":
            dots = VGroup()
            for _ in range(self.total_steps):
                d = Dot(radius=0.06 * self.width * 0.2)
                d.set_fill(t["progress_color"], 1.0)
                dots.add(d)
            dots.arrange(RIGHT, buff=0.18)
            self.progress_group = dots
        elif style == "bar":
            bar_w = self.width - 2 * t["panel_padding"]
            bar_h = t["progress_bar_height"]
            full = Rectangle(width=bar_w, height=bar_h, stroke_opacity=0, fill_opacity=0.25, fill_color=t["progress_color"])
            filled = Rectangle(width=0.0001, height=bar_h, stroke_opacity=0, fill_opacity=1.0, fill_color=t["progress_active_color"])
            filled.move_to(full.get_left(), LEFT)
            self.progress_group = VGroup(full, filled)

    def _layout_inside(self):
        t = self.theme
        pad = t["panel_padding"]

        # Subject at top-left inside panel (no indexing)
        ul = self.bg.get_corner(UL)            # 3D vector
        self.subject.move_to(ul + np.array([pad, -pad, 0.0]))
        self.subject.shift(0.01 * LEFT)

        # Headline under subject
        self.step_headline.next_to(self.subject, DOWN, buff=0.18)
        self.step_headline.align_to(self.subject, LEFT)

        # Progress indicator
        if len(self.progress_group) > 0:
            if t["progress_style"] == "dots":
                self.progress_group.scale(0.8)
                self.progress_group.next_to(self.subject, RIGHT, buff=0.35)
                # align right edge with panel’s right edge
                self.progress_group.align_to(self.bg, RIGHT)
            elif t["progress_style"] == "bar":
                y = bottom_y(self.bg) + t["panel_padding"] + t["progress_bar_padding"]
                self.progress_group.move_to(np.array([0.0, float(y), 0.0]))

        # Body
        self.body.set_max_width(self.inner_width * t["max_body_width_ratio"])
        self.body.next_to(self.step_headline, DOWN, buff=0.16)
        self.body.align_to(self.step_headline, LEFT)

    def set_subject(self, text):
        t = self.theme
        self.subject.become(_make_text(text, t, t["title_size"] / 48))
        self._layout_inside()

    def set_total_steps(self, n):
        self.total_steps = n
        self._rebuild_progress()
        self._layout_inside()

    def _activate_progress(self, idx):
        t = self.theme
        if t["progress_style"] == "dots" and len(self.progress_group) > 0:
            for i, dot in enumerate(self.progress_group):
                dot.set_fill(t["progress_color"], 1.0)
                if i <= idx - 1:
                    dot.set_fill(t["progress_active_color"], 1.0)
        elif t["progress_style"] == "bar" and len(self.progress_group) == 2:
            full, filled = self.progress_group
            if self.total_steps > 1:
                ratio = np.clip(idx / self.total_steps, 0, 1)
                new_w = max(ratio * full.width, 0.0001)
                nr = Rectangle(width=new_w, height=full.height, stroke_opacity=0, fill_opacity=1.0, fill_color=t["progress_active_color"])
                nr.move_to(full.get_left(), LEFT)
                filled.become(nr)

    def _make_body(self, text):
        t = self.theme
        lines = []
        for raw in text.split("\n"):
            if raw.strip().startswith(("- ", "• ")):
                lines.append(f"• {raw.strip()[2:]}")
            else:
                lines.append(raw)
        p = _make_paragraph(lines, t, t["body_size"] / 24)
        p.set_max_width(self.inner_width * t["max_body_width_ratio"])
        return p

    def update_step(self, scene, headline, body_text, step_index, animate=True):
        t = self.theme
        new_head = _make_text(headline, t, t["step_size"] / 48).align_to(self.subject, LEFT)
        new_head.next_to(self.subject, DOWN, buff=0.18)

        new_body = self._make_body(body_text)
        new_body.next_to(new_head, DOWN, buff=0.16).align_to(new_head, LEFT)

        self._activate_progress(step_index)

        if animate:
            scene.play(Transform(self.step_headline, new_head, run_time=t["transition_time"]))
            scene.play(Transform(self.body, new_body, run_time=t["transition_time"]))
        else:
            self.step_headline.become(new_head)
            self.body.become(new_body)

        self._layout_inside()

# ---------- SCRIPTED ENGINE ----------
def merge_theme(script):
    theme = DEFAULT_THEME.copy()
    if "theme" in script and isinstance(script["theme"], dict):
        theme.update({k: v for k, v in script["theme"].items() if k in theme})
    if "subject" in script:
        theme["subject"] = script["subject"]
    if "progress" in script:
        theme["progress_style"] = script["progress"]
    return theme

class ScriptedScene(MovingCameraScene):  # MovingCameraScene so .camera.frame exists
    SCRIPT = None           # set by your main.py subclass (or factory)
    VISUALS_CLS = None      # set to a class with action_*(...) methods

    def construct(self):
        assert self.SCRIPT is not None, "No SCRIPT bound."
        assert self.VISUALS_CLS is not None, "No VISUALS_CLS bound."

        theme = merge_theme(self.SCRIPT)

        # Panel
        total_steps = (1 if self.SCRIPT.get("intro") else 0) + len(self.SCRIPT.get("steps", []))
        self.panel = StepPanel(self.camera.frame, theme, total_steps=total_steps)
        self.panel.set_subject(theme["subject"])

        self.play(FadeIn(self.panel.bg, run_time=theme["appear_time"]))
        self.play(FadeIn(self.panel.subject, shift=0.1 * UP, run_time=theme["appear_time"]))

        # Visualization area geometry (no indexing)
        safe_top = top_y(self.panel.bg)
        gap = 0.2
        viz_height = top_y(self.camera.frame) - (safe_top + gap)

        # Build visuals object (user-defined)
        self.visuals = self.VISUALS_CLS(scene=self, panel_top=safe_top, available_height=viz_height)
        if hasattr(self.visuals, "build"):
            self.visuals.build()

        # Intro
        idx = 0
        intro = self.SCRIPT.get("intro")
        if intro:
            idx = 1
            self.panel.update_step(self, intro.get("title", ""), intro.get("body", ""), step_index=idx, animate=True)
            self.wait(theme["default_hold"])

        # Steps
        for s in self.SCRIPT.get("steps", []):
            idx += 1
            title = s.get("title", "")
            body = s.get("body", "")
            action = s.get("action")
            args = s.get("args", {}) or {}
            hold = s.get("wait", theme["default_hold"])

            self.panel.update_step(self, title, body, step_index=idx, animate=True)

            if action:
                fn = getattr(self.visuals, f"action_{action}", None)
                if fn:
                    fn(**args)
                elif hasattr(self.visuals, "run"):
                    self.visuals.run(action, **args)
                else:
                    print(f"[WARN] No visuals function for action '{action}'")

            self.wait(hold)

# (Optional) Factory if you prefer creating scenes programmatically in main.py
def make_scene(scene_name: str, script: dict, visuals_cls: type, module_name: str | None = None) -> type:
    class _Bound(ScriptedScene):
        SCRIPT = script
        VISUALS_CLS = visuals_cls
    _Bound.__name__ = scene_name
    if module_name:
        _Bound.__module__ = module_name
    return _Bound
