from manim import *
from manim_physics import *

class DoublePendulum(SpaceScene):
    def construct(self):
        p = MultiPendulum(RIGHT, LEFT)
        self.add(p)
        self.make_rigid_body(*p.bobs)
        p.start_swinging()
        self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
        self.wait(20)

class DoublePendulumExample(SpaceScene):
    def construct(self):
        pendulum = MultiPendulum(
            ORIGIN * 3,
            LEFT * 1.5
            )

        pendulum.bobs[0].mass = 1
        pendulum.bobs[1].mass = 2
        self.add(pendulum)

        self.make_rigid_body(*pendulum.bobs)

        pendulum.start_swinging()

        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=BLUE)
        self.add(trace)

        self.wait(20)

class TriplePendulumExample(SpaceScene):
    def construct(self):
        pendulum = MultiPendulum(ORIGIN, LEFT, RIGHT)

        self.add(pendulum)
        self.make_rigid_body(*pendulum.bobs)
        pendulum.start_swinging()

        # Spur des letzten Pendelkörpers
        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=RED)
        self.add(trace)

        self.wait(10)

class CustomTriplePendulum(SpaceScene):
    def construct(self):
        pendulum = MultiPendulum(
            ORIGIN,                
            ORIGIN + 2 * LEFT,     
            ORIGIN + LEFT + DOWN   
        )

        for i, bob in enumerate(pendulum.bobs):
            bob.mass = (i + 1) * 0.5  

        colors = [RED, GREEN, BLUE] 
        for i, bob in enumerate(pendulum.bobs):
            bob.set_color(colors[i])

        self.add(pendulum)

        self.make_rigid_body(*pendulum.bobs)

        pendulum.start_swinging()

        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=YELLOW)
        self.add(trace)

        self.wait(10)

class MultiSegmentPendulum(SpaceScene):
    def construct(self):
        anchor_points = [
            ORIGIN * LEFT + DOWN,
            ORIGIN + 1 * LEFT,
            ORIGIN,
            ORIGIN + 0.5 ,
        ]

        pendulum = MultiPendulum(*anchor_points)
        for i, bob in enumerate(pendulum.bobs):
           bob.mass = (i + 1) * 0.5  
        colors = [RED, GREEN,PURPLE, BLUE, ORANGE]
        for i, bob in enumerate(pendulum.bobs):
            bob.set_color(colors[i % len(colors)])

        self.add(pendulum)

        self.make_rigid_body(*pendulum.bobs)

        pendulum.start_swinging()

        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=WHITE)
        self.add(trace) 

        self.wait(20)
