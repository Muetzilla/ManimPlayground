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
        # Erstelle ein Doppelpendel mit Startpunkten
        pendulum = MultiPendulum(ORIGIN, LEFT)

        # Füge das Pendel zur Szene hinzu
        self.add(pendulum)

        # Mache die Massen zu physikalischen Objekten
        self.make_rigid_body(*pendulum.bobs)

        # Starte die Bewegung
        pendulum.start_swinging()

        # Spur des letzten Pendelkörpers hinzufügen
        trace = TracedPath(pendulum.bobs[-1].get_center, stroke_color=BLUE)
        self.add(trace)

        # Animation laufen lassen
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
        # Erstelle ein Pendel mit verschiedenen Längen
        pendulum = MultiPendulum(
            ORIGIN,                # Erster Punkt
            ORIGIN + 2 * LEFT,     # Zweiter Punkt (längerer Stab)
            ORIGIN + LEFT + DOWN   # Dritter Punkt (kürzerer Stab)
        )

        # Massen anpassen (Massen sind die Kreise, die als "bobs" bezeichnet werden)
        for i, bob in enumerate(pendulum.bobs):
            bob.mass = (i + 1) * 0.5  # Masse variiert pro Segment

        # Farben anpassen
        colors = [RED, GREEN, BLUE]  # Farben für die Pendelmasse
        for i, bob in enumerate(pendulum.bobs):
            bob.set_color(colors[i])

        # Das Pendel zur Szene hinzufügen
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
