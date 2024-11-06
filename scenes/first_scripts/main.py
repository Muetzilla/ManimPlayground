from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation


class SquareAndCircle(Scene):
    def construct(self):

        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        arrow = Arrow(LEFT, RIGHT)

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency
        
        circle2 = Circle()  # create a circle
        circle2.set_fill(ORANGE, opacity=0.5)  # set the color and transparency

        arrow2 = Arrow(RIGHT, LEFT)

        square2 = Square()  # create a square
        square2.set_fill(GREEN, opacity=0.5)  # set the color and transparency
        
        VGroup(square, arrow, circle).move_to(UP).set_x(0).arrange(buff=1.5).set_y(3)
       # VGroup(square, arrow, circle)move_to(UP).set_x(0).arrange(buff=1.5).set_y(3)
        VGroup(square2, arrow2, circle2).move_to(DOWN).set_x(0).arrange(buff=1.5).set_y(-3)

        self.play(Create(square))
        self.wait(0.5)
        self.play(GrowArrow(arrow))
        self.wait(0.5)
        self.play(Create(circle))
        self.wait(0.5)
        self.play(Create(circle2))
        self.wait(0.5)
        self.play(GrowArrow(arrow2))
        self.wait(0.5)
        self.play(Create(square2))
        self.wait(0.1)


class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello World")
        text.set_fill(RED, opacity=0.75)

        self.play(Create(text))

