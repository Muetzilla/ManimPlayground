from manim import *
import numpy as np

class ThreeBodyProblem(Scene):
    def construct(self):
        # Titel hinzufügen
        title = Text("Dreikörperproblem", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Kamera auf 9:16-Format und näher heranzoomen
        self.camera.frame_width = 30  # Zoomstufe einstellen

        # Anfangsbedingungen (Massen, Positionen und Geschwindigkeiten)
        masses = np.array([10, 20, 30], dtype=float)  # Massen der Körper

        positions = np.array([
            [-10, 10, -11],  # Startposition von Planet 1
            [0, 0, 0],       # Startposition von Planet 2
            [10, 10, 12]     # Startposition von Planet 3
        ], dtype=float)

        velocities = np.array([
            [-3, 0, 0],  # Startgeschwindigkeit von Planet 1
            [0, 0, 0],   # Startgeschwindigkeit von Planet 2
            [3, 0, 0]    # Startgeschwindigkeit von Planet 3
        ], dtype=float)

        # Punkte für die Körper mit besserer Qualität
        dots = VGroup(
            *[Dot(color=color, radius=0.15).move_to([pos[0], pos[1], 0]) for pos, color in zip(positions, [BLUE, RED, GREEN])]
        )

        self.add(dots)

        # Trajektorienlinien
        trails = []
        for pos, color in zip(positions, [BLUE, RED, GREEN]):
            trail = VMobject(stroke_color=color, stroke_width=2)
            # Stelle sicher, dass der Pfad initialisiert wird
            trail.start_new_path(np.array([pos[0], pos[1], 0]))
            trails.append(trail)
            self.add(trail)

        # Gravitationskraft berechnen
        def gravitational_force(pos1, pos2, m1, m2):
            r_vec = pos2 - pos1  # Vektor von pos1 nach pos2
            r = np.linalg.norm(r_vec)  # Betrag des Vektors
            if r == 0:
                return np.zeros(3)  # Vermeide Division durch 0
            return (r_vec / r) * (m1 * m2) / r**2  # Normalisierte Kraft

        # Simulation: Aktualisiere Positionen und Geschwindigkeiten
        def update_positions_and_velocities(dt):
            nonlocal positions, velocities  # Zugriff auf die äußeren Variablen
            forces = np.zeros_like(positions, dtype=float)  # Kräfte als float64 initialisieren
            for i in range(len(positions)):
                for j in range(len(positions)):
                    if i != j:
                        forces[i] += gravitational_force(
                            positions[i], positions[j], masses[i], masses[j]
                        )
            # Aktualisiere Geschwindigkeiten und Positionen
            for i in range(len(positions)):
                velocities[i] += forces[i] * dt / masses[i]
                positions[i] += velocities[i] * dt

        # Bewegung der Punkte animieren
        def update_dots():
            for i, dot in enumerate(dots):
                dot.move_to([positions[i][0], positions[i][1], 0])

            # Aktualisiere die Trajektorien
            for i, trail in enumerate(trails):
                new_point = np.array([positions[i][0], positions[i][1], 0])
                trail.add_line_to(new_point)

        # Simuliere die Bewegung für mehrere Frames
        dt = 0.01
        num_frames = 1000
        for frame in range(num_frames):
            update_positions_and_velocities(dt)
            update_dots()
            self.wait(0.01)

        # Szene abschließen
        self.wait(2)
