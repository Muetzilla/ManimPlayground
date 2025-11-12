# visuals/template.py
from manim import *
import numpy as np

class Visuals:
    def __init__(self, scene: Scene, panel_top: float, available_height: float):
        self.scene = scene
        self.panel_top = float(panel_top)
        self.available_height = float(available_height)
        self.group = None

    def _center_y(self):
        gap = 0.2
        return self.panel_top + gap + self.available_height / 2.0

    def build(self):
        circle = Circle().set_stroke(opacity=0.8)
        circle.move_to(np.array([0.0, float(self._center_y()), 0.0]))  # 3D point
        self.group = circle

    def action_show_scene(self):
        self.scene.play(FadeIn(self.group))

    def action_do_something(self, speed=1.0):
        self.scene.play(Rotate(self.group, angle=TAU), run_time=1.0 / max(speed, 0.01))

    def run(self, name, **kwargs):
        fn = getattr(self, f"action_{name}", None)
        if fn:
            return fn(**kwargs)
