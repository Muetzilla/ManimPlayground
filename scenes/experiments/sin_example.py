from manim import *

class SinExample(Scene):
    def construct(self):
        # Create a sine wave function
        wave = FunctionGraph(lambda x: np.sin(x), x_range=[-PI, PI], color=BLUE)
        self.play(Create(wave))
        self.wait(1)
        
        # Animate the wave moving and changing
        for _ in range(5):
            new_wave = FunctionGraph(lambda x: np.sin(x + _ * 0.5), x_range=[-PI, PI], color=BLUE)
            self.play(Transform(wave, new_wave), run_time=0.5)
            self.wait(0.1)
        
        self.wait(2)