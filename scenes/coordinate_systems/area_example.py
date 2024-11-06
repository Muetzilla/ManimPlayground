from manim import *

#With Area
class GetAreaExample(Scene):
    def construct(self):
        ax = Axes().add_coordinates()
        curve = ax.plot(lambda x: 2 * np.sin(x), color=DARK_BLUE)
        area = ax.get_area(
            curve,
            x_range=(PI / 2, 3 * PI / 2),
            color=(GREEN_B, GREEN_D),
            opacity=1,
        )

        self.add(ax, curve, area)

# With Label
class GetGraphLabelExample(Scene):
    def construct(self):
        ax = Axes()
        sin = ax.plot(lambda x: np.sin(x), color=PURPLE_B)
        label = ax.get_graph_label(
            graph=sin,
            label= MathTex(r"\frac{\pi}{2}"),
            x_val=PI / 2,
            dot=True,
            direction=UR,
        )

        self.add(ax, sin, label)