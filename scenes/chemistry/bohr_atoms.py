from manim import *
from manim_chemistry import *

class DrawBohrDiagram(Scene):
    def construct(self):
        diagram = BohrAtom(e=14, p=14, n=10)
        self.add(diagram)


class DrawBohrDiagramRotating(Scene):
    def construct(self):
        self.play(
            Rotate(
                BohrAtom(e=14, p=14, n=10).scale(0.5),
                angle=2*PI,
                about_point=ORIGIN,
                rate_func=linear,
            ),
            run_time=5
            )