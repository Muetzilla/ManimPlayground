from manim import *
import numpy as np

class SinFunction(Scene):
    def construct(self):
        #Sin function
        sinCoordSystem = Axes(x_range=[0, 20, 2], x_length = 10, y_range=[-2, 2, 1], y_length=6)
        sinCoordSystem.add_coordinates()
        sinFunction = sinCoordSystem.plot(lambda x : np.sin(x), x_range=[0, 20], color = BLUE)
        sinLabel = MathTex("sin(x)").next_to(sinCoordSystem, UP, buff=0.2).set_color(BLUE)
        sinGroup = VGroup(sinCoordSystem, sinLabel, sinFunction)

        #Cosin function
        cosinCoordSystem = Axes(x_range=[0, 20, 2], x_length = 10, y_range=[-2, 2, 1], y_length=6)
        cosinCoordSystem.add_coordinates()
        cosinFunction = cosinCoordSystem.plot(lambda x : np.cos(x), x_range=[0, 20], color = RED)
        cosinLabel = MathTex("cos(x)").next_to(cosinCoordSystem, UP, buff=0.2).set_color(RED)
        cosinGroup = VGroup(cosinCoordSystem, cosinLabel, cosinFunction)

        combinedGroup = VGroup(sinGroup, cosinGroup)
        arrow = Arrow(LEFT, RIGHT)

        #Combined function
        combinedCorrdSystem = Axes(x_range=[0, 20, 2], x_length = 10, y_range=[-3, 3, 1], y_length=6)
        combinedCorrdSystem.add_coordinates()
        combinedFunction = combinedCorrdSystem.plot(lambda x : np.sin(x) + np.cos(x), x_range=[0, 20], color = PURPLE)
        combinedLabel = MathTex("sin(x) + cos(x)").next_to(combinedCorrdSystem, UP, buff=0.2).set_color(PURPLE)
        combinedCoordGroup = VGroup(combinedCorrdSystem, combinedLabel, combinedFunction)
        combinedCoordGroup.scale(0.375)
        combinedCoordGroup.to_edge(RIGHT)

        self.play(DrawBorderThenFill(sinCoordSystem))
        self.play(Create(sinFunction, run_time = 3), Write(sinLabel))
        self.wait(1)
        self.play(FadeOut(sinGroup))
        self.wait(0.2)
        self.play(DrawBorderThenFill(cosinCoordSystem))
        self.play(Create(cosinFunction, run_time = 3), Write(cosinLabel))
        self.wait(1)
        sinGroup.scale(0.5).to_edge(UP)
        self.play(cosinGroup.animate.scale(0.5).to_edge(DOWN), FadeIn(sinGroup))
        self.wait(0.5)
        self.play(combinedGroup.animate.scale(0.75).to_edge(LEFT))
        self.wait(0.7)
        self.play(GrowArrow(arrow))
        self.wait(0.7)
        self.play(DrawBorderThenFill(combinedCorrdSystem))
        self.play(Create(combinedFunction, run_time = 4), Write(combinedLabel))
        self.wait(0.1)


