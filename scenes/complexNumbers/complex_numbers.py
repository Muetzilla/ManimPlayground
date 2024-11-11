from manim import *

class NormalForm(Scene):
    def construct(self):
        normalFormLabel = MathTex('a + bi').set_color(BLUE)
        realPartLabel = MathTex('Re(a)').set_color(GREEN)
        imaginaryPartLabel = MathTex('Im(b)').set_color(RED)
        sqrtMinusOne = MathTex('i (\sqrt{-1})').set_color(PURPLE)
        sqrtMinusOne.move_to(RIGHT)
        plusLabel = MathTex('+')
        multiplication = MathTex('*')
        multiplication.move_to(RIGHT)
        sqrtMinusOne.next_to(multiplication)
        arrow = Arrow(LEFT, RIGHT, color=BLUE).next_to(normalFormLabel, LEFT)
        textGroup = VGroup(normalFormLabel, arrow, sqrtMinusOne, realPartLabel, imaginaryPartLabel, plusLabel, multiplication)

        complexNumberPlane = ComplexPlane().add_coordinates()
        

        d1 = Dot(complexNumberPlane.n2p(2 + 1j), color=YELLOW)
        d2 = Dot(complexNumberPlane.n2p(-3 - 2j), color=YELLOW)
        label1 = MathTex("2+i").next_to(d1, UR, 0.1)
        label2 = MathTex("-3-2i").next_to(d2, UR, 0.1)


        complexGroup = VGroup(complexNumberPlane, d1, label1, d2, label2)
        complexGroup.scale(0.75)

        self.add(normalFormLabel)
        self.wait(0.5)
        self.play(normalFormLabel.animate.to_edge(LEFT))
        self.wait(0.3)
        self.play(GrowArrow(arrow))
        self.play(arrow.animate.next_to(normalFormLabel, RIGHT))
        self.wait(0.1)
        self.add(realPartLabel)
        self.wait(0.5)
        self.play(realPartLabel.animate.next_to(arrow, RIGHT))
        self.add(plusLabel)
        self.wait(0.1)
        self.play(plusLabel.animate.next_to(realPartLabel, RIGHT))
        self.add(imaginaryPartLabel)
        self.wait(0.5)
        self.play(imaginaryPartLabel.animate.next_to(plusLabel, RIGHT))
        self.add(multiplication)
        self.wait(0.5)
        self.play(multiplication.animate.next_to(imaginaryPartLabel, RIGHT))
        self.add(sqrtMinusOne)
        self.wait(0.5)
        self.play(sqrtMinusOne.animate.next_to(multiplication, RIGHT))
        self.wait(1)
        self.play(FadeOut(textGroup))
        self.add(complexNumberPlane)
        self.play(Create(d1), Create(label1, run_time = 2))
        self.wait(0.5)
        self.play(Create(d2), Create(label2, run_time = 1))
        self.wait(1)
      