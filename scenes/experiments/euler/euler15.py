"""
Manim-Erklärvideo zu Project Euler Problem 15 (Gitterpfade)
===========================================================

Ziel des Videos: Hintergründe und Denkweisen verstehen -- NICHT die fertige
Lösung vorführen. Am Ende soll der Zuschauer selbst auf eine Implementierung
kommen.

Rendern (niedrige Qualität, schnell):
    manim -pql euler15_manim.py Euler15Erklaerung

Rendern (Full HD):
    manim -pqh euler15_manim.py Euler15Erklaerung

Es wird kein LaTeX benötigt (nur Text-Objekte).
"""

from itertools import permutations

import numpy as np
from manim import *

# ----------------------------------------------------------------------------
# Farben
# ----------------------------------------------------------------------------
C_RIGHT = BLUE_C      # Schritt nach rechts
C_DOWN = RED_C        # Schritt nach unten
C_PATH = YELLOW       # gezeichneter Weg
C_GRID = GREY_B       # Gitterlinien
C_HIGHLIGHT = GREEN_C


# ----------------------------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------------------------
def txt(s, size=32, color=WHITE, max_w=12.0):
    """Text mit begrenzter Breite, damit nichts aus dem Bild läuft."""
    t = Text(s, font_size=size, color=color)
    if t.width > max_w:
        t.scale_to_fit_width(max_w)
    return t


def node_pos(r, c, n, sp, center=ORIGIN):
    """Position des Knotens (Zeile r, Spalte c) in einem Gitter mit n x n Feldern.
    (0, 0) ist links oben, (n, n) rechts unten."""
    return center + np.array([(c - n / 2) * sp, (n / 2 - r) * sp, 0.0])


def build_grid(n, sp, center=ORIGIN, dots=True, stroke=2, color=C_GRID):
    """Gitter mit n x n Feldern (also (n+1) x (n+1) Knoten)."""
    lines = VGroup()
    for r in range(n + 1):
        for c in range(n + 1):
            if c < n:
                lines.add(Line(node_pos(r, c, n, sp, center),
                               node_pos(r, c + 1, n, sp, center),
                               stroke_width=stroke, color=color))
            if r < n:
                lines.add(Line(node_pos(r, c, n, sp, center),
                               node_pos(r + 1, c, n, sp, center),
                               stroke_width=stroke, color=color))
    grid = VGroup(lines)
    if dots:
        d = VGroup(*[
            Dot(node_pos(r, c, n, sp, center), radius=0.07, color=WHITE)
            for r in range(n + 1) for c in range(n + 1)
        ])
        grid.add(d)
    return grid


def route_mobject(word, n, sp, center=ORIGIN, color=C_PATH, stroke=6):
    """Zeichnet einen Weg aus einem Wort wie 'RRDD' (R = rechts, D = down)."""
    r = c = 0
    pts = [node_pos(r, c, n, sp, center)]
    for ch in word:
        if ch == "R":
            c += 1
        else:
            r += 1
        pts.append(node_pos(r, c, n, sp, center))
    path = VMobject()
    path.set_points_as_corners(pts)
    path.set_stroke(color=color, width=stroke)
    return path


def word_mobject(word, size=36):
    """Wort aus R/D, jeder Buchstabe farbig."""
    letters = VGroup(*[
        Text(ch, font_size=size, color=C_RIGHT if ch == "R" else C_DOWN, weight=BOLD)
        for ch in word
    ])
    letters.arrange(RIGHT, buff=0.25)
    return letters


# ----------------------------------------------------------------------------
# Die Szene
# ----------------------------------------------------------------------------
class Euler15Erklaerung(Scene):
    def construct(self):
        self.intro_und_problem()
        self.warum_nicht_aufzaehlen()
        self.idee_lokal_denken()
        self.idee_umformulieren()
        self.abschluss()

    # ------------------------------------------------------------------
    # 1. Problem verstehen
    # ------------------------------------------------------------------
    def intro_und_problem(self):
        title = txt("Project Euler 15: Gitterpfade", size=46, color=YELLOW)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # kleines Beispiel: 2x2 Felder
        n, sp = 2, 1.5
        center = LEFT * 3.2 + DOWN * 0.3
        grid = build_grid(n, sp, center)
        start = txt("Start", 26, GREEN_C).next_to(node_pos(0, 0, n, sp, center), UL, buff=0.1)
        ziel = txt("Ziel", 26, RED_C).next_to(node_pos(n, n, n, sp, center), DR, buff=0.1)
        self.play(Create(grid), run_time=2)
        self.play(FadeIn(start), FadeIn(ziel))

        # Regeln
        row1 = VGroup(Arrow(ORIGIN, RIGHT * 0.8, color=C_RIGHT, buff=0),
                      txt("nur nach rechts", 28)).arrange(RIGHT, buff=0.3)
        row2 = VGroup(Arrow(ORIGIN, DOWN * 0.8, color=C_DOWN, buff=0),
                      txt("oder nach unten", 28)).arrange(RIGHT, buff=0.3)
        row3 = txt("Nie zurück, nie diagonal.", 26, GREY_A)
        rules = VGroup(txt("Erlaubte Schritte:", 30, YELLOW), row1, row2, row3)
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.6 + DOWN * 0.2)
        self.play(FadeIn(rules, shift=LEFT * 0.3))
        self.wait(1)

        # zwei Beispielwege
        for w in ["RRDD", "RDRD"]:
            p = route_mobject(w, n, sp, center)
            self.play(Create(p), run_time=2)
            self.wait(0.5)
            self.play(FadeOut(p))

        frage = txt("Wie viele verschiedene Wege führen von Start nach Ziel?", 32, WHITE)
        frage.to_edge(DOWN, buff=0.5)
        self.play(Write(frage))
        self.wait(2)

        self.play(FadeOut(VGroup(grid, start, ziel, rules, frage)))

        # alle 6 Wege
        words = sorted(set("".join(p) for p in permutations("RRDD")))
        minis = VGroup()
        for i, w in enumerate(words):
            ctr = np.array([-4 + 4 * (i % 3), 0.9 - 2.8 * (i // 3), 0.0])
            g = build_grid(2, 0.9, ctr, stroke=1.5)
            p = route_mobject(w, 2, 0.9, ctr, stroke=5)
            minis.add(VGroup(g, p))
        self.play(LaggedStart(*[FadeIn(m) for m in minis], lag_ratio=0.3), run_time=3)
        count = txt("Bei 2 × 2 Feldern gibt es genau 6 Wege. Abzählen geht noch.", 30)
        count.to_edge(DOWN, buff=0.4)
        self.play(Write(count))
        self.wait(2)
        self.play(FadeOut(minis), FadeOut(count))

        # das echte Problem: 20x20
        n, sp = 20, 0.27
        center = LEFT * 3.5 + DOWN * 0.4
        big = build_grid(n, sp, center, dots=False, stroke=1)
        s2 = txt("Start", 24, GREEN_C).next_to(node_pos(0, 0, n, sp, center), UL, buff=0.05)
        z2 = txt("Ziel", 24, RED_C).next_to(node_pos(n, n, n, sp, center), DR, buff=0.05)
        side = txt("Das eigentliche Problem:\n20 × 20 Felder.\n\nDieselbe Frage -\naber zeichnen und\nabzählen ist keine\nOption mehr.", 30)
        side.move_to(RIGHT * 3.8)
        self.play(Create(big), run_time=2)
        self.play(FadeIn(s2), FadeIn(z2), Write(side))
        self.wait(3)
        # Titel mit ausblenden, damit er später nicht unter den Überschriften steht
        self.play(FadeOut(VGroup(big, s2, z2, side, title)))

    # ------------------------------------------------------------------
    # 2. Warum Brute Force an Grenzen stößt
    # ------------------------------------------------------------------
    def warum_nicht_aufzaehlen(self):
        kopf = txt("Alle Wege einzeln erzeugen?", 40, YELLOW).move_to(UP * 2.4)
        self.play(Write(kopf))

        zeilen = VGroup(
            txt("Ein Weg im 20 × 20 Gitter besteht aus 40 Schritten.", 30),
            txt("Bei jedem Schritt: rechts oder unten.", 30),
            txt("Der Suchraum wächst mit jedem Feld enorm.", 30),
        ).arrange(DOWN, buff=0.45).next_to(kopf, DOWN, buff=0.6)
        for z in zeilen:
            self.play(FadeIn(z, shift=UP * 0.2))
            self.wait(0.7)

        # Wachstum an kleinen Gittern zeigen
        gr = VGroup()
        for k, num in zip([1, 2, 3], ["2", "6", "20"]):
            g = build_grid(k, 0.55, ORIGIN, stroke=1.5)
            lab = txt(f"{k} × {k}:  {num} Wege", 24)
            gr.add(VGroup(g, lab).arrange(DOWN, buff=0.3))
        gr.arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(gr, shift=UP * 0.3))
        self.wait(1)
        hint = txt("Das wächst viel schneller als das Gitter selbst.", 26, YELLOW)
        hint.next_to(gr, UP, buff=0.3)
        self.play(Write(hint))
        self.wait(2.5)

        # Frage in den Raum stellen
        self.play(FadeOut(VGroup(zeilen, gr, hint)))
        frage = txt("Gibt es eine Struktur im Problem,\ndie wir ausnutzen können?", 38, WHITE)
        frage.move_to(ORIGIN)
        self.play(Write(frage))
        self.wait(2)
        self.play(FadeOut(frage), FadeOut(kopf))

    # ------------------------------------------------------------------
    # 3. Idee A: Lokal denken (jeder Knoten für sich)
    # ------------------------------------------------------------------
    def idee_lokal_denken(self):
        kopf = txt("Idee 1: Frag nicht nach dem ganzen Weg,\nsondern nur nach dem letzten Schritt", 34, YELLOW)
        kopf.move_to(UP * 3.0)
        self.play(Write(kopf))

        n, sp = 2, 1.9
        center = LEFT * 3.0 + DOWN * 0.7
        P = lambda r, c: node_pos(r, c, n, sp, center)
        grid = build_grid(n, sp, center, dots=False, stroke=2)
        circles = {(r, c): Circle(radius=0.36, color=WHITE, stroke_width=2,
                                  fill_color=BLACK, fill_opacity=1).move_to(P(r, c))
                   for r in range(n + 1) for c in range(n + 1)}
        self.play(Create(grid), FadeIn(VGroup(*circles.values())))

        # Frage: woher kann man in einen Knoten kommen?
        target = (1, 1)
        self.play(circles[target].animate.set_color(C_HIGHLIGHT).set_stroke(width=5))
        erkl = txt("Auf welchen Wegen kann ich\nan diesem Knoten ankommen?", 28)
        erkl.move_to(RIGHT * 3.8 + UP * 1.5)
        self.play(Write(erkl))
        self.wait(1)

        a_left = Arrow(P(1, 0), P(1, 1), buff=0.4, color=C_RIGHT, stroke_width=8)
        a_top = Arrow(P(0, 1), P(1, 1), buff=0.4, color=C_DOWN, stroke_width=8)
        self.play(GrowArrow(a_left), GrowArrow(a_top))
        antwort = txt("Nur von links (Schritt →)\noder von oben (Schritt ↓).", 28)
        antwort.next_to(erkl, DOWN, buff=0.5)
        self.play(Write(antwort))
        self.wait(2)

        regel = txt("Jeder Weg hierher endet also in einem dieser\nbeiden Schritte - und davor war er schon\nein Weg zum linken bzw. oberen Nachbarn.", 24, GREY_A)
        regel.next_to(antwort, DOWN, buff=0.5)
        self.play(FadeIn(regel))
        self.wait(4)
        self.play(FadeOut(VGroup(a_left, a_top, erkl, antwort, regel)),
                  circles[target].animate.set_color(WHITE).set_stroke(width=2))

        # Rand: nur eine Möglichkeit
        info = txt("Und am Rand? Dort gibt es nur\nein einziger Weg - immer geradeaus.", 28)
        info.move_to(RIGHT * 3.8 + UP * 1.5)
        self.play(Write(info))

        labels = {}

        def make_label(rc, val, color=WHITE):
            lab = Text(str(val), font_size=34, color=color).move_to(P(*rc))
            labels[rc] = lab
            return lab

        rand = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]
        self.play(*[Write(make_label(rc, 1)) for rc in rand])
        self.wait(1)
        self.play(FadeOut(info))

        # Innere Knoten befüllen
        werte = {rc: 1 for rc in rand}
        calc = None
        for rc in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            r, c = rc
            left, top = (r, c - 1), (r - 1, c)
            a = werte[left]
            b = werte[top]
            neu = a + b

            self.play(circles[rc].animate.set_color(C_HIGHLIGHT).set_stroke(width=5))
            self.play(Indicate(labels[left], color=C_RIGHT, scale_factor=1.5),
                      Indicate(labels[top], color=C_DOWN, scale_factor=1.5))

            neu_calc = txt(f"{a}  +  {b}  =  {neu}", 40)
            neu_calc.move_to(RIGHT * 3.8 + UP * 1.0)
            if calc is None:
                self.play(FadeIn(neu_calc))
            else:
                self.play(FadeTransform(calc, neu_calc))
            calc = neu_calc

            werte[rc] = neu
            self.play(Write(make_label(rc, neu, YELLOW)))
            self.play(circles[rc].animate.set_color(WHITE).set_stroke(width=2))
            self.wait(0.3)

        # Abgleich mit dem Abzählen
        self.play(circles[(2, 2)].animate.set_color(YELLOW).set_stroke(width=6))
        check = txt("Im Ziel steht dieselbe Zahl wie beim\nAbzählen der 6 Wege vorhin.", 28, GREEN_C)
        check.move_to(RIGHT * 3.8 + DOWN * 0.5)
        self.play(FadeOut(calc), Write(check))
        self.wait(3)

        fragen = VGroup(
            txt("Zum Nachdenken für deine Implementierung:", 28, YELLOW),
            txt("• Welche Datenstruktur bildet dieses Gitter ab?", 26),
            txt("• In welcher Reihenfolge füllst du die Knoten?", 26),
            txt("• Warum ist die Reihenfolge überhaupt wichtig?", 26),
            txt("• Was musst du wirklich gleichzeitig speichern?", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        fragen.move_to(RIGHT * 3.6 + DOWN * 1.2)
        self.play(FadeOut(check))
        fragen.move_to(RIGHT * 3.6 + UP * 0.2)
        for f in fragen:
            self.play(FadeIn(f, shift=LEFT * 0.2), run_time=0.6)
            self.wait(0.5)
        self.wait(4)

        self.play(FadeOut(VGroup(kopf, grid, fragen,
                                 *circles.values(), *labels.values())))

    # ------------------------------------------------------------------
    # 4. Idee B: Den Weg umformulieren (Kombinatorik)
    # ------------------------------------------------------------------
    def idee_umformulieren(self):
        kopf = txt("Idee 2: Ein Weg ist nur eine Folge von Entscheidungen", 36, YELLOW)
        kopf.move_to(UP * 3.2)
        self.play(Write(kopf))

        n, sp = 2, 1.5
        center = LEFT * 4.0 + DOWN * 0.2
        grid = build_grid(n, sp, center)
        self.play(Create(grid))

        # Weg Schritt für Schritt zeichnen und in Buchstaben übersetzen
        word = "RDRD"
        r = c = 0
        buchstaben = VGroup()
        prev = node_pos(0, 0, n, sp, center)
        segmente = VGroup()
        for i, ch in enumerate(word):
            if ch == "R":
                c += 1
            else:
                r += 1
            nxt = node_pos(r, c, n, sp, center)
            seg = Line(prev, nxt, color=C_RIGHT if ch == "R" else C_DOWN, stroke_width=8)
            lab = Text(ch, font_size=40, color=C_RIGHT if ch == "R" else C_DOWN, weight=BOLD)
            lab.move_to(RIGHT * (1.0 + 0.8 * i) + UP * 1.5)
            self.play(Create(seg), FadeIn(lab, shift=DOWN * 0.2), run_time=0.8)
            segmente.add(seg)
            buchstaben.add(lab)
            prev = nxt
        legende = txt("R = Schritt nach rechts,  D = Schritt nach unten", 24, GREY_A)
        legende.move_to(RIGHT * 2.6 + UP * 2.4)
        self.play(FadeIn(legende))
        self.wait(1)

        beob = VGroup(
            txt("Jeder Weg ist ein 'Wort' aus R und D.", 28),
            txt("Alle Wege haben gleich viele R (2) und gleich", 28),
            txt("viele D (2) - also immer 4 Schritte.", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        beob.move_to(RIGHT * 2.6 + UP * 0.1)
        self.play(FadeIn(beob))
        self.wait(3)
        self.play(FadeOut(VGroup(grid, segmente, buchstaben, legende, beob)))

        # Alle Wörter nebeneinander
        words = sorted(set("".join(p) for p in permutations("RRDD")))
        spalten = VGroup()
        for w in words:
            spalten.add(word_mobject(w, 40))
        spalten.arrange_in_grid(rows=3, cols=2, buff=(1.5, 0.5))
        spalten.move_to(LEFT * 3.5 + DOWN * 0.3)
        self.play(LaggedStart(*[Write(s) for s in spalten], lag_ratio=0.25), run_time=3)

        kern = VGroup(
            txt("Ein Weg ist festgelegt, sobald du weißt,", 28),
            txt("an welchen Stellen ein R steht.", 28),
            txt("Alle übrigen Stellen sind dann", 28),
            txt("automatisch D.", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        kern.move_to(RIGHT * 3.4 + UP * 0.8)
        self.play(FadeIn(kern))
        self.wait(2)

        # Slots zeigen: aus 4 Plätzen werden 2 für R gewählt
        slots = VGroup(*[Square(side_length=0.7, color=WHITE) for _ in range(4)]).arrange(RIGHT, buff=0.15)
        slots.move_to(RIGHT * 3.4 + DOWN * 1.3)
        nums = VGroup(*[txt(str(i + 1), 20, GREY_A).next_to(s, DOWN, buff=0.1)
                        for i, s in enumerate(slots)])
        self.play(Create(slots), FadeIn(nums))
        wahl = [(0, 1), (0, 2)]
        for pair in wahl:
            marks = VGroup(*[
                Text("R", font_size=30, color=C_RIGHT, weight=BOLD).move_to(slots[i])
                for i in pair
            ])
            self.play(FadeIn(marks), run_time=0.5)
            self.wait(0.5)
            self.play(FadeOut(marks), run_time=0.3)

        frage = txt("Wie viele Möglichkeiten gibt es, aus 4 Plätzen\n2 für das R auszuwählen?", 26, YELLOW)
        frage.move_to(RIGHT * 3.4 + DOWN * 2.9)
        self.play(Write(frage))
        self.wait(3)
        self.play(FadeOut(VGroup(spalten, kern, slots, nums, frage)))

        # Übertragung auf 20x20 als Frage
        ueber = VGroup(
            txt("Im echten Problem:", 34, YELLOW),
            txt("40 Plätze, davon werden 20 für R gewählt.", 32),
            Dot(radius=0.01, color=BLACK),
            txt("Das ist ein klassisches Zählproblem der Kombinatorik.", 28),
            txt("Wie heißt es? Wie berechnet man es?", 28, GREEN_C),
            txt("Und worauf musst du bei großen Zahlen achten?", 28, GREEN_C),
        ).arrange(DOWN, buff=0.3)
        ueber.move_to(ORIGIN)
        for z in ueber:
            self.play(FadeIn(z, shift=UP * 0.2), run_time=0.7)
        self.wait(4)
        self.play(FadeOut(ueber), FadeOut(kopf))

    # ------------------------------------------------------------------
    # 5. Abschluss
    # ------------------------------------------------------------------
    def abschluss(self):
        kopf = txt("Zwei Sichtweisen auf dasselbe Problem", 40, YELLOW).move_to(UP * 2.8)
        self.play(Write(kopf))

        links = VGroup(
            txt("Lokal denken", 32, C_RIGHT),
            txt("Jeder Knoten hängt nur von", 24),
            txt("zwei Nachbarn ab.", 24),
            txt("→ Problem in kleine, gleich-", 24, GREY_A),
            txt("artige Teilprobleme zerlegen", 24, GREY_A),
        ).arrange(DOWN, buff=0.2)
        rechts = VGroup(
            txt("Umformulieren", 32, C_DOWN),
            txt("Weg = Folge aus R und D.", 24),
            txt("Zählen von Anordnungen.", 24),
            txt("→ Das Gitter verschwindet,", 24, GREY_A),
            txt("das Problem wird abstrakter", 24, GREY_A),
        ).arrange(DOWN, buff=0.2)
        VGroup(links, rechts).arrange(RIGHT, buff=1.5).move_to(ORIGIN + UP * 0.2)
        trenner = Line(UP * 1.5, DOWN * 1.5, color=GREY_B).move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(links, shift=RIGHT * 0.3), Create(trenner), FadeIn(rechts, shift=LEFT * 0.3))
        self.wait(3)

        aufgabe = VGroup(
            txt("Deine Aufgabe:", 30, YELLOW),
            txt("Setze beide Ideen in Code um und vergleiche", 26),
            txt("Aufwand, Speicherbedarf und Rechenzeit.", 26),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(aufgabe, shift=UP * 0.3))
        self.wait(5)

        self.play(FadeOut(VGroup(kopf, links, rechts, trenner, aufgabe)))
        ende = txt("Viel Erfolg beim Implementieren!", 40, GREEN_C)
        self.play(Write(ende))
        self.wait(2)
        self.play(FadeOut(ende))
