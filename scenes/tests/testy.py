from manim import *

class Test(Scene):
        def construct(self):
            MathTex("Hello World").scale(2).to_edge(UP)