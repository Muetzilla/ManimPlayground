from manim import *
from manim_chemistry import *

class DrawPOrbital(Scene):
    def construct(self):
        orbital = Orbital(l=1, m=-1)
        self.add(orbital)