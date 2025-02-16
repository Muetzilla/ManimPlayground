from manim import *
from manim_physics import *
import numpy as np

class DoublePendulum(SpaceScene):
    def construct(self):
        pendulum = MultiPendulum(
            ORIGIN * 0.5,
            LEFT * 0.75 + 1.25 * UP
        )

        pendulum.bobs[0].mass = 100
        pendulum.bobs[1].mass = 50

        pendulum.bobs[0].color = RED
        pendulum.bobs[1].color = GREEN

        self.add(pendulum)

        self.make_rigid_body(*pendulum.bobs)

        pendulum.start_swinging()

        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=BLUE)
        self.add(trace)

        def update_trace(trace, dt):
            elapsed_time = self.time
            new_color = interpolate_color(BLUE, RED, np.sin(elapsed_time) * 0.5 + 0.5)
            trace.set_stroke(color=new_color)

        trace.add_updater(update_trace)

        self.wait(20) 
        trace.remove_updater(update_trace)
        self.play(FadeOut(trace)) 
        self.wait(15) 