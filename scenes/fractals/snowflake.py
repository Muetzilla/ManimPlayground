from manim import *
import numpy as np

def koch_snowflake(order, start_points):
    """ Rekursive Funktion zur Erzeugung der Koch-Schneeflocke nach außen """
    if order == 0:
        return start_points
    new_points = []
    for i in range(len(start_points) - 1):
        p1 = start_points[i]
        p2 = start_points[i + 1]

        # Teilung der Strecke in 3 Teile
        a = p1
        b = p1 + (p2 - p1) / 3
        d = p1 + 2 * (p2 - p1) / 3
        c = b + (d - b) * np.exp(-1j * np.pi / 3)  # -60°-Drehung (nach außen)

        new_points.extend([a, b, c, d])
    new_points.append(start_points[-1])
    return new_points

class KochSnowflakeStepwise(Scene):
    def construct(self):  
        # Gleichseitiges Dreieck mit Basis oben (um 180° gedreht)
        triangle = [
            np.exp(1j * 0) * 3,          # Rechte Ecke
            np.exp(1j * 2*np.pi/3) * 3,  # Linke Ecke
            np.exp(1j * -2*np.pi/3) * 3, # Obere Ecke
            np.exp(1j * 0) * 3           # Zurück zur rechten Ecke
        ]
        triangle = np.array(triangle)  # <- Keine zusätzliche Einrückung hier!
        iterations = 5  # Anzahl der Iterationen

        # Start mit dem Grunddreieck
        current_points = triangle
        snowflake = VMobject()
        snowflake.set_points_as_corners([complex_to_R3(p) for p in current_points])
        snowflake.set_color(WHITE)

        self.play(Create(snowflake), run_time=2)
        self.wait(0.5)

        # Animation für jede Iteration
        for i in range(1, iterations + 1):
            next_points = koch_snowflake(1, current_points)
            next_snowflake = VMobject()
            next_snowflake.set_points_as_corners([complex_to_R3(p) for p in next_points])
            next_snowflake.set_color(WHITE)

            self.play(Transform(snowflake, next_snowflake), run_time=2)
            self.wait(0.5)
            current_points = next_points  # Update für die nächste Iteration

        self.wait()
