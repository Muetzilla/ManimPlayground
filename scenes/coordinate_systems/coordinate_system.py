from manim import *

class CoordinateSystem(Scene):
    def construct(self):
        my_plane = Axes(x_range=[-6, 6, 2], x_length = 8, y_range=[-10, 10, 2], y_length=6)
        my_plane.add_coordinates()

        my_function = my_plane.plot(lambda x : 0.1*(x-5)*x*(x+5), x_range=[-6, 6], color = GREEN_B)

        area = my_plane.get_area(graph = my_function, x_range=[-5,5], color = [BLUE, YELLOW])

        label = MathTex("f(x)=0.1x(x-5)(x+5)").next_to(my_plane, UP, buff=0.2)

        self.play(DrawBorderThenFill(my_plane))
        self.play(Create(my_function), Write(label))
        self.play(FadeIn(area))
       
