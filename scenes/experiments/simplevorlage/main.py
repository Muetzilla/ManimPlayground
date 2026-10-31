# simple_narrated_toptitle.py
# Title centered at the very top of the frame, narration panel stays below.

from manim import *
import numpy as np

SUBJECT = "Your Topic"
STEPS = [
    {"title": "Intro",  "body": "• What we'll cover\n• Visuals above, text below"},
    {"title": "Step 1", "body": "Explain the first idea clearly and concisely."},
    {"title": "Step 2", "body": "Explain the second idea.\n- bullet works\n• dot works"},
]

class SimpleNarrated(Scene):
    def construct(self):
        fw, fh = config.frame_width, config.frame_height

        # --- Panel geometry ---
        panel_h = fh * 0.25
        panel_margin = 0.1
        pad_x, pad_y = 0.3, 0.2

        # Position panel safely near bottom
        panel_bottom = -fh / 2 + panel_margin + panel_h * 0.15
        panel_y = panel_bottom + panel_h / 2
        panel_w = fw - 2 * panel_margin

        # --- Background panel ---
        panel_color = GREY_E
        bg = Rectangle(width=panel_w, height=panel_h)
        bg.set_fill(panel_color, 1).set_stroke(opacity=0)
        bg.move_to([0, panel_y, 0])
        self.add(bg)

        # --- Title centered at the very top ---
        title = Text(SUBJECT, color=WHITE, weight=BOLD).scale(0.4)
        top_y = fh / 2 - 0.4   # small margin from the top
        title.move_to([0, top_y, 0])
        self.play(FadeIn(title, shift=0.3*UP, run_time=0.6))

        # --- Placeholders (hidden) ---
        headline = Text(".", color=panel_color).scale(0.25)
        body = Text(".", color=panel_color).scale(0.25)
        self.add(headline, body)

        # --- Visualization area ---
        viz_gap = 0.25
        viz_y = panel_y + panel_h / 2 + viz_gap + 1.0
        dot = Dot().move_to([0, viz_y, 0])
        self.play(FadeIn(dot, run_time=0.35))

        # --- Helper for body text ---
        def make_body(text):
            lines = []
            for raw in text.split("\n"):
                s = raw.strip()
                lines.append(f"• {s[2:]}" if s.startswith(("- ", "• ")) else raw)
            return Paragraph(*lines, alignment="left", line_spacing=0.7).scale(0.23)

        # Layout constants
        title_gap = 0.3
        line_gap = 0.2

        def update_panel(step_title, body_text):
            nonlocal headline, body
            new_h = Text(step_title, color=WHITE).scale(0.25)
            hx = -fw/2 + panel_margin + pad_x + new_h.width/2
            hy = panel_y + panel_h/2 - pad_y - new_h.height/2 - 0.1
            new_h.move_to([hx, hy, 0])

            new_b = make_body(body_text)
            new_b.set_max_width((panel_w - 2*pad_x) * 0.9)
            bx = -fw/2 + panel_margin + pad_x + new_b.width/2
            by = new_h.get_bottom()[1] - line_gap - new_b.height/2
            min_y = panel_y - panel_h / 2 + pad_y
            if by - new_b.height/2 < min_y:
                by = min_y + new_b.height/2
            new_b.move_to([bx, by, 0])

            self.play(ReplacementTransform(headline, new_h, run_time=0.4))
            self.play(ReplacementTransform(body, new_b, run_time=0.4))
            headline, body = new_h, new_b

        # --- Run steps ---
        if STEPS:
            update_panel(STEPS[0]["title"], STEPS[0]["body"]); self.wait(0.4)
        for step in STEPS[1:]:
            update_panel(step["title"], step["body"])
            self.play(dot.animate.shift(0.6*RIGHT), run_time=0.3)
            self.play(dot.animate.shift(0.6*LEFT), run_time=0.3)
            self.wait(0.25)

        self.play(FadeOut(dot), run_time=0.3)

__all__ = ["SimpleNarrated"]
