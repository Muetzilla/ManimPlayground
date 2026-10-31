from manim import *
import numpy as np

def top_y(mobj: Mobject) -> float:
    return float(mobj.get_y() + mobj.height / 2)

class Visuals:
    def __init__(self, scene: Scene, panel_top: float, available_height: float):
        self.scene = scene
        self.panel_top = float(panel_top)
        self.available_height = float(available_height)

        self.values = [3, 1, 4, 2, 5]
        self.bars = None

    def _center_y(self):
        gap = 0.2
        return self.panel_top + gap + self.available_height / 2.0

    def build(self):
        max_val = max(self.values)
        bars = VGroup()
        width = 0.6
        for v in self.values:
            h = 0.9 * self.available_height * (v / max_val)
            bar = Rectangle(width=width, height=h).set_fill(opacity=1.0).set_stroke(opacity=0.0)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.25)
        # Place with explicit 3D point (no indexing)
        bars.move_to(np.array([0.0, float(self._center_y()), 0.0]))
        self.bars = bars

    # ---- Actions used by the script ----
    def action_show_array(self):
        self.scene.play(FadeIn(self.bars), run_time=0.6)

    def action_scan(self, start=0):
        anims = []
        for i in range(start, len(self.bars)):
            anims.append(self.bars[i].animate.set_stroke(color=YELLOW_A, width=6))
            anims.append(self.bars[i].animate.set_stroke(opacity=0.0))
        self.scene.play(AnimationGroup(*anims, lag_ratio=0.15))

    def action_swap(self, i=0, j=1):
        if 0 <= i < len(self.bars) and 0 <= j < len(self.bars):
            left = self.bars[i]
            right = self.bars[j]
            offset = (right.get_center()[0] - left.get_center()[0]) * RIGHT
            self.scene.play(left.animate.shift(offset), right.animate.shift(-offset), run_time=0.8)
            # swap in the VGroup list
            self.bars.submobjects[i], self.bars.submobjects[j] = self.bars.submobjects[j], self.bars.submobjects[i]

    def action_repeat_hint(self):
        self.scene.play(self.bars.animate.set_opacity(0.7), run_time=0.2)
        self.scene.play(self.bars.animate.set_opacity(1.0), run_time=0.2)

    def run(self, name, **kwargs):
        fn = getattr(self, f"action_{name}", None)
        if fn:
            return fn(**kwargs)
