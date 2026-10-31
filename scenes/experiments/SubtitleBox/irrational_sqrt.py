from manim import *
from subtitle_box.box import SubtitleBox 

class Sqrt2ContinuedFraction(Scene):
    def construct(self):
        # -------------------------------------------------------
        # TITLE
        # -------------------------------------------------------
        title = Tex(r"\(\sqrt{2}\) ist irrational (Kettenbruch-Beweis)")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # -------------------------------------------------------
        # EQUATIONS – PHASE 1 (x-Gleichungen)
        # -------------------------------------------------------
        eq1 = MathTex("x^2", "=", "2").shift(UP * 2)
        eq2 = MathTex("x^2", "-", "1", "=", "1").move_to(eq1)
        eq3 = MathTex("(", "x", "-", "1", ")", "(", "x", "+", "1", ")", "=", "1").move_to(eq1)
        eq4 = MathTex("x", "-", "1", "=", r"\frac{1}{", "x", "+", "1", "}").move_to(eq1)

        # -------------------------------------------------------
        # SUBTITLE BOX
        # -------------------------------------------------------
        sub = SubtitleBox("")
        self.play(FadeIn(sub))

        # -------------------------------------------------------
        # PHASE 1 ANIMATION
        # -------------------------------------------------------
        # Step 1: x^2 = 2
        highlight_box = SurroundingRectangle(eq1, buff=0.12, color=YELLOW)
        highlight_box.set_stroke(width=4)

        self.play(Write(eq1))
        self.play(Create(highlight_box))
        self.play(sub.set_text("Starte mit der Gleichung: x² = 2"))
        self.wait(0.8)

        # Step 2: x^2 - 1 = 1
        eq2[1].set_color(RED)
        eq2[2].set_color(RED)

        self.play(TransformMatchingTex(eq1, eq2, transform_mismatched_size=False))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(eq2, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Subtrahiere 1 auf beiden Seiten: x² - 1 = 1"))
        self.wait(0.8)

        # Step 3: (x-1)(x+1) = 1
        for i in range(0, 10):
            eq3[i].set_color(RED)

        self.play(TransformMatchingTex(eq2, eq3, transform_mismatched_size=False))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(eq3, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Faktorisieren: x² - 1 = (x - 1)(x + 1)"))
        self.wait(0.8)

        # Step 4: x - 1 = 1 / (x+1)
        eq4[0].set_color(RED)
        eq4[1].set_color(RED)
        eq4[2].set_color(RED)
        eq4[5].set_color(RED)
        eq4[6].set_color(RED)
        eq4[7].set_color(RED)

        self.play(TransformMatchingTex(eq3, eq4, transform_mismatched_size=False))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(eq4, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Teile durch (x + 1): x - 1 = 1 / (x + 1)"))
        self.wait(1)

        # -------------------------------------------------------
        # PHASE 2 – y und Kettenbruch
        # -------------------------------------------------------
        self.play(FadeOut(highlight_box), FadeOut(eq4))

        # y = x - 1
        eq5 = MathTex("y", "=", "x", "-", "1").shift(UP * 2)
        eq5[0].set_color(YELLOW)
        eq5[2].set_color(RED)
        eq5[3].set_color(RED)
        eq5[4].set_color(RED)

        highlight_box = SurroundingRectangle(eq5, buff=0.12, color=YELLOW)

        self.play(Write(eq5))  # Übergang von x-1 zu y
        self.play(Create(highlight_box))

        #self.play(Transform(highlight_box, SurroundingRectangle(eq5, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Definiere y = x - 1."))
        self.wait(0.8)

        # Platz schaffen: frühere Zeilen weg
        self.play(FadeOut(eq5), FadeOut(highlight_box))

        # y = 1 / (2 + y)  (erste Gleichung)
        step1 = MathTex("y", "=", r"\frac{1}{", "2", "+", "y", "}").shift(UP*0.5)
        step1[0].set_color(YELLOW)
        step1[3].set_color(RED)
        step1[4].set_color(RED)
        step1[5].set_color(RED)

        highlight_box = SurroundingRectangle(step1, buff=0.12, color=YELLOW)

        self.play(FadeIn(step1, shift=DOWN*0.2))
        self.play(Create(highlight_box))
        self.play(sub.set_text("Wir setzen unsere Gleichung in die rechte Seite ein: y = 1 / (2 + y)."))
        self.wait(1)

        # gelbes Rahmen-Rechteck für die „Zoom“-Ansicht des Kettenbruchs
        box = Rectangle(
            width=step1.width + 1,
            height=3.5,
            color=YELLOW
        )
        box.surround(step1, buff=0.7)
        self.play(Create(box))
        self.wait(0.3)

        # Schritt 2: y wieder einsetzen → eine Stufe tiefer
        step2 = MathTex(
            "y", "=", r"\frac{1}{", "2", "+",
            r"\frac{1}{", "2", "+", "y", "}", "}"
        )
        step2[0].set_color(YELLOW)
        for i in [3, 4, 6, 7, 8]:
            step2[i].set_color(RED)
        step2.move_to(step1)

        self.play(Transform(step1, step2))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(step1, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Nun setzen wir y erneut auf der rechten Seite ein – der Bruch wird tiefer."))
        self.wait(1)

        # Schritt 3: noch einmal einsetzen
        step3 = MathTex(
            "y", "=", r"\frac{1}{", "2", "+",
            r"\frac{1}{", "2", "+",
            r"\frac{1}{", "2", "+", "y", "}", "}", "}"
        )
        step3[0].set_color(YELLOW)
        for i in [3, 4, 6, 7, 9, 10, 11]:
            step3[i].set_color(RED)
        step3.move_to(step1)

        self.play(Transform(step1, step3))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(step1, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Wenn wir das immer weiter machen, taucht immer wieder 2 + ... im Nenner auf."))
        self.wait(1)

        # Schritt 4: ersetze das letzte y durch „…“ → unendlicher Kettenbruch
        cf = MathTex(
            r"y", "=", r"\cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{2 + \ddots}}}"
        )
        cf[0].set_color(YELLOW)
        cf.move_to(step1)

        self.play(Transform(step1, cf))
        self.play(Transform(highlight_box,
                            SurroundingRectangle(cf, buff=0.12, color=YELLOW)))
        self.play(sub.set_text("Im Grenzfall erhalten wir einen unendlichen Kettenbruch für y."))
        self.wait(1.5)

        # Schluss: x = 1 + y = √2
        x_final = MathTex("x", "=", "1", "+", "y", "=", r"\sqrt{2}")
        x_final[0].set_color(YELLOW)
        x_final[-1].set_color(RED)
        x_final.next_to(cf, DOWN, buff=0.6)

        self.play(FadeOut(box), FadeOut(highlight_box))
        self.play(FadeIn(x_final, shift=DOWN*0.2))
        highlight_box = SurroundingRectangle(x_final, buff=0.12, color=YELLOW)
        self.play(Create(highlight_box))
        self.play(sub.set_text(
            "Dieser unendliche Kettenbruch hat den Wert x = √2. "
            "Da rationale Zahlen nur endliche Kettenbrüche haben, ist √2 irrational."
        ))
        self.wait(2)

        # Finale Box → grün
        result_box = SurroundingRectangle(x_final, buff=0.12, color=GREEN)
        result_box.set_stroke(width=5)
        self.play(Transform(highlight_box, result_box))
        self.wait(2)
        
        self.play(FadeOut(sub), FadeOut(title), FadeOut(step1), FadeOut(x_final), FadeOut(highlight_box))
        self.wait(1)
