from manim import *

class FibonacciSequence(Scene):
    def construct(self):
        self.camera.background_color = BLACK  # Set background to black for a cool effect

        # Define gradient colors and font globally
        gradient_colors = [BLUE, TEAL, GREEN]  # Gradient from blue to green
        font_style = "Times New Roman"

        title = Text(
            "Fibonacci Sequence", 
            font_size=36, 
            gradient=gradient_colors,  # Use global gradient
            font=font_style  # Use global font
        )
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Define the first few Fibonacci numbers
        fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21]
        fib_equations = []

        for i in range(2, len(fib_numbers)):
            equation_before = MathTex(
                f"F_{i} = F_{{{i-1}}} + F_{{{i-2}}}",
                font_size=64, color=BLUE
            )
            equation_after = MathTex(
                f"{fib_numbers[i]} = {fib_numbers[i-1]} + {fib_numbers[i-2]}",
                font_size=64, color=GREEN
            )
            equation_before.move_to(ORIGIN)
            equation_after.move_to(ORIGIN)
            
            self.play(Write(equation_before))
            self.wait(1)
            self.play(Transform(equation_before, equation_after))  # Morphing effect
            self.wait(1)
            self.play(FadeOut(equation_before))
            self.wait(0.5)
        
        self.play(FadeOut(title))
