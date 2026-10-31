from manim import *
from subtitle_box.box import SubtitleBox 

class TestScene(Scene):
    def construct(self):
        title = Tex(r"Lineare Gleichung Schritt für Schritt lösen")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Gleichungen teilbar machen
        eq1 = MathTex("2x", "+", "3", "=", "11")
        eq2 = MathTex("2x", "=", "11", "-", "3")
        eq3 = MathTex("2x", "=", "8")
        eq4 = MathTex(r"\frac{2x}{2}", "=", r"\frac{8}{2}")
        eq5 = MathTex("x", "=", "4")

        equations = VGroup(eq1, eq2, eq3, eq4, eq5)
        equations.arrange(DOWN, buff=0.4)
        equations.center()
        equations.shift(UP * 0.75)

        # -------------------------------------------------------
        # GELBE BOX UM AKTIVE ZEILE
        # -------------------------------------------------------
       
        # -------------------------------------------------------

        # Schritt 1
        sub = SubtitleBox("")
        self.play(FadeIn(sub))
        highlight_box = SurroundingRectangle(eq1, buff=0.12, color=YELLOW)
        highlight_box.set_stroke(width=4)

        self.play(Write(eq1))
        self.play(Create(highlight_box))
        self.play(sub.set_text("Ausgangsgleichung: 2x + 3 = 11"))
        self.wait(0.8)

      
        # Schritt 2 — roter Teil
        eq2[3].set_color(RED)
        eq2[4].set_color(RED)

        self.play(FadeIn(eq2, shift=DOWN*0.2))
        self.play(Transform(highlight_box, SurroundingRectangle(eq2, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Subtrahiere 3 auf beiden Seiten."))
        self.wait(0.8)

        # Schritt 3 — roter Teil
        eq3[2].set_color(RED)

        self.play(FadeIn(eq3, shift=DOWN*0.2))
        self.play(Transform(highlight_box, SurroundingRectangle(eq3, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("11 - 3 = 8, dadurch wird es zu: 2x = 8"))
        self.wait(0.8)

        # Schritt 4
        eq4[0].set_color(RED)
        eq4[2].set_color(RED)

        self.play(FadeIn(eq4, shift=DOWN*0.2))
        self.play(Transform(highlight_box, SurroundingRectangle(eq4, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Teile beide Seiten durch 2."))
        self.wait(0.8)

        # Schritt 5
        eq5[2].set_color(RED)

        self.play(FadeIn(eq5, shift=DOWN*0.2))
        self.play(Transform(highlight_box, SurroundingRectangle(eq5, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Ergebnis: x = 4"))
        self.wait(1)

        # finale Box → grün (für Ergebnis)
        result_box = SurroundingRectangle(eq5, buff=0.12, color=GREEN)
        result_box.set_stroke(width=5)
        self.play(Transform(highlight_box, result_box))
        self.wait(2)
