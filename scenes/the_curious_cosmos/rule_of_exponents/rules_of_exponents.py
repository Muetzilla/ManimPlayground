from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class ExponentLaws(Scene):
    def construct(self):
        self.camera.background_color = BLACK  
        title = Text(
            "Laws of Exponents", 
            font_size=72, 
            gradient=(BLUE, TEAL, GREEN),
            font="Times New Roman"  
        )
        title.to_edge(UP, buff=2.5) 
        self.play(Write(title))
        self.wait(1)

        rules = [
            ("Product Rule:", "a^m \cdot a^n", "a^{m+n}", ""),
            ("Quotient Rule:", "\\frac{a^m}{a^n}" , "a^{m-n}",  "\\text{provided that a}  \\neq 0"),
            ("Power Rule:", "(a^m)^n", "a^{m \cdot n}", ""),
            ("Negative Rule:", "a^{-n}", "\\frac{1}{a^n}", ""),
            ("Multiplication Rule:", "a^m \cdot b^m", "(a \cdot b)^m", ""),
            ("Division Rule:", r"\frac{a^m}{b^m}", r"\left(\frac{a}{b}\right)^m", ""),
        ]

        for rule_name, initial_expr, transformed_expr, additional_content in rules:
            name = Text(rule_name, font_size=28, gradient=(PURPLE, PINK, RED), font="Times New Roman")
            name.to_edge(UP, buff=1.5)
            equation_before = MathTex(initial_expr, font_size=64, color=WHITE)
            equation_after = MathTex(transformed_expr, font_size=64, color=WHITE)
            equation_before.move_to(ORIGIN)
            equation_after.move_to(ORIGIN)
            additional_info = MathTex("additional_content", font_size=32, color=WHITE)
            additional_info.to_edge(DOWN)
            self.play(Write(equation_before))
            self.wait(1)
            
            self.play(Transform(equation_before, equation_after))
            self.wait(1)
            
            self.play(FadeOut(equation_before))
        
        self.play(FadeOut(title))
