"""
YouTube-Thumbnail zur Cäsar-Chiffre (Manim Community Edition)

Als PNG rendern (nur das Standbild, keine Animation):
    manim -s -r 1280,720 caesar_thumbnail.py Thumbnail      # YouTube-Standardgröße
    manim -s -r 1920,1080 caesar_thumbnail.py Thumbnail     # höhere Auflösung

Die Datei landet in  media/images/caesar_thumbnail/Thumbnail_ManimCE_*.png
(YouTube erlaubt Thumbnails bis 2 MB, empfohlen: 1280x720, 16:9.)

Layout: links der Titel, rechts der Chiffrier-Ring, unten links ein Beispiel.
Alle Elemente liegen in getrennten Zonen, nichts überlagert sich.
"""
from manim import *
import numpy as np

BG = "#10131f"
PLAIN = BLUE_C
CIPHER = YELLOW
OK = GREEN_C
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SHIFT = 3


def fit(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ---------------- Hintergrund-Akzent ----------------
        glow = Circle(radius=3.6, fill_color=PLAIN, fill_opacity=0.10, stroke_width=0)
        glow.move_to([3.9, 0, 0])
        self.add(glow)

        # ---------------- Titel (links) ----------------
        line1 = Text("CÄSAR", font_size=120, weight=BOLD, color=WHITE)
        line2 = Text("CHIFFRE", font_size=120, weight=BOLD, color=CIPHER)
        fit(line1, 6.4)
        fit(line2, 6.4)
        title = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        title.move_to([-6.7, 0.7, 0], aligned_edge=LEFT)
        self.add(title)

        bar = Line(LEFT, RIGHT, color=PLAIN, stroke_width=8).set_width(2.4)
        bar.next_to(title, DOWN, buff=0.35, aligned_edge=LEFT)
        self.add(bar)

        # ---------------- Beispiel (links unten) ----------------
        example = VGroup(
            Text("HALLO", font_size=52, weight=BOLD, color=PLAIN),
            Text("→", font_size=52, color=WHITE),
            Text("KDOOR", font_size=52, weight=BOLD, color=CIPHER),
        ).arrange(RIGHT, buff=0.4)
        example.move_to([-6.7, -2.8, 0], aligned_edge=LEFT)
        self.add(example)

        # ---------------- Ring (rechts) ----------------
        c = np.array([3.9, 0.0, 0.0])

        def pos(idx, r):
            a = PI / 2 - TAU * idx / 26
            return c + r * np.array([np.cos(a), np.sin(a), 0])

        self.add(Circle(radius=2.38, color=GRAY, stroke_width=2, stroke_opacity=0.6).move_to(c))
        self.add(Circle(radius=1.55, color=GRAY, stroke_width=2, stroke_opacity=0.35).move_to(c))

        for i, ch in enumerate(ALPHA):
            # außen: Klartext
            self.add(Text(ch, font_size=34, weight=BOLD, color=PLAIN).move_to(pos(i, 2.72)))
            # innen: Geheimtext, um 3 Stellen gedreht (Buchstabe i steht an Position i - 3)
            self.add(Text(ch, font_size=30, weight=BOLD, color=CIPHER).move_to(pos(i - SHIFT, 2.05)))

        # Hervorgehobenes Paar: A (außen) ↔ D (innen)
        a_out = Text("A", font_size=48, weight=BOLD, color=OK).move_to(pos(0, 2.72))
        d_in = Text("D", font_size=42, weight=BOLD, color=OK).move_to(pos(0, 2.05))
        self.add(a_out, d_in)

        # Kleiner Schlüssel-Hinweis in der Ringmitte
        key = VGroup(
            Text("k", font_size=40, color=WHITE),
            Text("= 3", font_size=40, color=WHITE),
        ).arrange(RIGHT, buff=0.15).move_to(c)
        self.add(key)
