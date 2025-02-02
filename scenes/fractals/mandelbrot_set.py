from manim import *

class MandelbrotSet(Scene):
    def construct(self):
        title = Text("Mandelbrot-Set").to_edge(UP)
        self.play(Write(title))

        axes = ComplexPlane(
            x_range=[-2, 1, 1],
            y_range=[-1.5, 1.5, 1],
            faded_line_ratio=2,
        ).add_coordinates()
        self.play(Create(axes))

        def mandelbrot(c, max_iter=50):
            z = 0
            for n in range(max_iter):
                if abs(z) > 2:
                    return n / max_iter
                z = z * z + c
            return 0

        pixels = VGroup()
        for x in np.linspace(-2, 1, 200):
            for y in np.linspace(-1.5, 1.5, 200):
                c = complex(x, y)
                color = interpolate_color(BLACK, BLUE, mandelbrot(c))
                pixel = Dot(axes.c2p(x, y), radius=0.01, color=color)
                pixels.add(pixel)

        self.play(FadeIn(pixels), run_time=5)

        self.wait(2)
        self.play(FadeOut(*self.mobjects))
