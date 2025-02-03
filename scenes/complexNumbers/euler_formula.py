from manim import *

class EulerFormula(Scene):
    def construct(self):
        title = Text("Eulerformel und komplexe Zahlen").to_edge(UP)
        self.play(Write(title))

        plane = ComplexPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            faded_line_ratio=2,
        ).add_coordinates()

        self.play(Create(plane))

        # Kreis für e^(iθ)
        circle = Circle(radius=1, color=YELLOW)
        self.play(Create(circle))

        dot = Dot(color=RED)
        dot.move_to(circle.point_from_proportion(0))
        self.add(dot)

        line = always_redraw(
            lambda: Line(plane.c2p(0, 0), dot.get_center(), color=BLUE)
        )
        self.add(line)

        euler_formula = MathTex("e^{i\\theta} = \\cos(\\theta) + i\\sin(\\theta)").to_edge(DOWN)
        self.play(Write(euler_formula))

        theta_label = always_redraw(
            lambda: MathTex(
                "\\theta = " + f"{np.arctan2(dot.get_center()[1], dot.get_center()[0]):.2f}"
            ).next_to(euler_formula, UP)
        )
        self.add(theta_label)

        self.play(MoveAlongPath(dot, circle, rate_func=linear), run_time=8)

        self.wait(2)
        self.play(FadeOut(*self.mobjects))
