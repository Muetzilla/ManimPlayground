from manim import *

class FourierSeries(Scene):
    def construct(self):
        title = Text("Fourier-Reihen").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"include_tip": False},
            tips=False,
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        self.play(Create(axes), Write(axes_labels))

        square_wave = axes.plot(
            lambda x: 1 if (x % (2 * PI)) < PI else -1,
            color=YELLOW,
        )
        square_label = axes.get_graph_label(
            square_wave, label="f(x)", x_val=2, direction=UP
        )

        self.play(Create(square_wave), Write(square_label))

        # Fourier-Summen erstellen
        def fourier_series(x, n):
            sum_value = 0
            for k in range(1, n + 1, 2):  
                sum_value += (4 / (k * PI)) * np.sin(k * x)
            return sum_value

        fourier_graphs = []
        for n in range(1, 20, 2):  
            fourier_graph = axes.plot(
                lambda x, n=n: fourier_series(x, n), color=BLUE
            )
            fourier_graphs.append(fourier_graph)

        self.play(*[Create(graph) for graph in fourier_graphs], run_time=5, lag_ratio=0.5)

        final_graph = axes.plot(lambda x: fourier_series(x, 19), color=GREEN)
        self.play(Transform(fourier_graphs[-1], final_graph), run_time=2)

        self.wait(2)
        self.play(FadeOut(*self.mobjects))
