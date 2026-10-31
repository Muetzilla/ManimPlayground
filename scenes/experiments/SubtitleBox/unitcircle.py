from manim import *
from subtitle_box.box import SubtitleBox
import numpy as np


class UnitCircleScene(Scene):
    def construct(self):
        # -------------------------------------------------------
        # TITEL
        # -------------------------------------------------------
        title = Tex(r"Sinus und Cosinus am Einheitskreis")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # -------------------------------------------------------
        # SUBTITLE-BOX (Box bleibt gleich, Text kannst du intern verkleinern)
        # -------------------------------------------------------
        sub = SubtitleBox("")
        self.play(FadeIn(sub))

        def set_subtitle(text):
            """Hilfsfunktion für Untertitel.
            Wenn deine SubtitleBox z.B. ein Attribut 'text' hat,
            kannst du dort die Schriftgröße anpassen.
            """
            self.play(sub.set_text(text))
            # Beispiel – nur verwenden, wenn deine SubtitleBox so aufgebaut ist:
            # if hasattr(sub, "text"):
            #     self.play(sub.text.animate.scale(0.8))

        set_subtitle("Wir starten mit dem Einheitskreis im Koordinatensystem.")

        # -------------------------------------------------------
        # KOORDINATENSYSTEM + EINHEITSKREIS (AM ANFANG IN DER MITTE)
        # -------------------------------------------------------
        axes = NumberPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=4,
            y_length=4,
        )
        circle = Circle(radius=1, color=BLUE)

        self.play(Create(axes), Create(circle))
        self.wait(0.5)

        # Radius 1 markieren
        radius_line_x = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        radius_label = MathTex("1").scale(0.7).next_to(radius_line_x, DOWN * 0.5)
        self.play(Create(radius_line_x), FadeIn(radius_label))
        set_subtitle("Der Einheitskreis hat Radius 1 und liegt im Ursprung.")

        # -------------------------------------------------------
        # WINKEL, PUNKT, DREIECK, SIN & COS
        # -------------------------------------------------------
        theta = ValueTracker(PI / 4)

        def get_point():
            return circle.point_at_angle(theta.get_value())

        # Radius
        radius_line = always_redraw(
            lambda: Line(axes.c2p(0, 0), get_point(), color=YELLOW)
        )
        moving_dot = always_redraw(
            lambda: Dot(get_point(), color=YELLOW)
        )

        # Winkelbogen
        angle_arc = always_redraw(
            lambda: Arc(
                start_angle=0,
                angle=theta.get_value(),
                radius=0.4,
                color=YELLOW,
                arc_center=axes.c2p(0, 0),
            )
        )
        angle_label = MathTex(r"\alpha").scale(0.8)
        angle_label.add_updater(
            lambda m: m.next_to(angle_arc, RIGHT * 0.4 + UP * 0.1)
        )

        self.play(Create(radius_line), FadeIn(moving_dot))
        self.play(Create(angle_arc), FadeIn(angle_label))
        set_subtitle("Wir wählen einen Winkel \\(\\alpha\\). Der Punkt liegt auf dem Einheitskreis.")

        # Projektion auf die x-Achse
        def get_projection_x():
            p = get_point()
            return np.array([p[0], axes.c2p(0, 0)[1], 0])

        horizontal_leg = always_redraw(
            lambda: Line(axes.c2p(0, 0), get_projection_x(), color=GREEN)
        )
        vertical_leg = always_redraw(
            lambda: Line(get_projection_x(), get_point(), color=RED)
        )

        self.play(Create(horizontal_leg))
        self.play(Create(vertical_leg))
        set_subtitle("Wir ergänzen ein rechtwinkliges Dreieck zur x-Achse.")

        # Beschriftung der Seiten
        cos_label = MathTex(r"\cos(\alpha)").scale(0.7)
        sin_label = MathTex(r"\sin(\alpha)").scale(0.7)

        cos_label.add_updater(
            lambda m: m.next_to(horizontal_leg, DOWN, buff=0.3).shift(0.2 * LEFT)
        )
        sin_label.add_updater(
            lambda m: m.next_to(vertical_leg, RIGHT, buff=0.3).shift(0.1 * UP)
        )

        self.play(Write(cos_label))
        set_subtitle("Die waagerechte Seite hat die Länge \\(\\cos(\\alpha)\\).")

        self.play(Write(sin_label))
        set_subtitle("Die senkrechte Seite hat die Länge \\(\\sin(\\alpha)\\).")

        coord_label = MathTex(r"(\cos(\alpha), \sin(\alpha))").scale(0.7)
        coord_label.add_updater(
            lambda m: m.next_to(moving_dot, UP * 0.7)
        )
        self.play(FadeIn(coord_label, shift=UP * 0.2))
        set_subtitle("Der Punkt hat die Koordinaten \\((\\cos(\\alpha), \\sin(\\alpha))\\).")

        self.wait(1)

        # -------------------------------------------------------
        # GRUPPE LINKS BILDEN (SPÄTER NACH LINKS SCHIEBEN)
        # -------------------------------------------------------
        left_group = VGroup(
            axes, circle, radius_line_x, radius_label,
            radius_line, moving_dot,
            angle_arc, angle_label,
            horizontal_leg, vertical_leg,
            cos_label, sin_label, coord_label
        )

        # -------------------------------------------------------
        # RECHTE SEITE: ACHSEN FÜR SINUS UND COSINUS
        # -------------------------------------------------------
        graph_axes = Axes(
            x_range=[0, TAU, PI / 2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=5,
            y_length=3,
            tips=False,
        )

        # Einheitskreis nach links, Graph-Achsen nach rechts
        self.play(left_group.animate.to_edge(LEFT, buff=1))
        graph_axes.to_edge(RIGHT, buff=1)

        x_label = MathTex(r"\alpha").scale(0.7).next_to(graph_axes.x_axis, DOWN)
        y_label = MathTex(r"\sin(\alpha),\,\cos(\alpha)").scale(0.7).next_to(
            graph_axes.y_axis, LEFT
        )

        self.play(Create(graph_axes))
        self.play(FadeIn(x_label), FadeIn(y_label))
        set_subtitle("Rechts tragen wir den Winkel \\(\\alpha\\) gegen Sinus und Cosinus auf.")

        sin_text = MathTex(r"\sin(\alpha)").scale(0.7).set_color(RED)
        cos_text = MathTex(r"\cos(\alpha)").scale(0.7).set_color(BLUE)
        sin_text.next_to(graph_axes, UP, buff=0.3)
        cos_text.next_to(sin_text, RIGHT, buff=0.7)

        self.play(FadeIn(sin_text), FadeIn(cos_text))
        self.wait(0.5)

        # -------------------------------------------------------
        # ERSTE RUNDE: GRAPHS ENTSTEHEN (MIT TRACEDPATH)
        # -------------------------------------------------------
        # Startwinkel auf 0 setzen
        self.play(theta.animate.set_value(0), run_time=1)
        set_subtitle("Wir starten bei \\(\\alpha = 0\\) und lassen den Punkt einmal umlaufen.")

        sin_dot_trace = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(
                    theta.get_value(), np.sin(theta.get_value())
                ),
                radius=0.06,
                color=RED,
            )
        )
        cos_dot_trace = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(
                    theta.get_value(), np.cos(theta.get_value())
                ),
                radius=0.06,
                color=BLUE,
            )
        )

        sin_trace = TracedPath(
            sin_dot_trace.get_center,
            stroke_color=RED,
            stroke_width=3,
        )
        cos_trace = TracedPath(
            cos_dot_trace.get_center,
            stroke_color=BLUE,
            stroke_width=3,
        )

        self.add(sin_trace, cos_trace, sin_dot_trace, cos_dot_trace)

        self.play(theta.animate.set_value(TAU), run_time=8, rate_func=linear)
        set_subtitle("Dabei entstehen die Graphen von \\(\\sin(\\alpha)\\) und \\(\\cos(\\alpha)\\).")
        self.wait(1)

        # -------------------------------------------------------
        # SPUREN AUSBLENDEN, FERTIGE GRAPHEN ZEICHNEN
        # -------------------------------------------------------
        sin_graph = graph_axes.plot(lambda x: np.sin(x), x_range=[0, TAU], color=RED)
        cos_graph = graph_axes.plot(lambda x: np.cos(x), x_range=[0, TAU], color=BLUE)

        # Spuren weg, Graphen „sauber“ zeichnen
        self.play(FadeOut(sin_trace), FadeOut(cos_trace), FadeOut(sin_dot_trace), FadeOut(cos_dot_trace))
        self.play(Create(sin_graph), Create(cos_graph), run_time=2)

        set_subtitle("Das sind die vollständigen Kurven von Sinus und Cosinus.")
        self.wait(1.5)

        # -------------------------------------------------------
        # WEITERE RUNDEN: PUNKTE AUF FERTIGEN GRAPHS
        # -------------------------------------------------------
        moving_sin_dot = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(
                    theta.get_value(), np.sin(theta.get_value())
                ),
                radius=0.06,
                color=RED,
            )
        )
        moving_cos_dot = always_redraw(
            lambda: Dot(
                graph_axes.coords_to_point(
                    theta.get_value(), np.cos(theta.get_value())
                ),
                radius=0.06,
                color=BLUE,
            )
        )

        self.add(moving_sin_dot, moving_cos_dot)

        set_subtitle("Schauen wir uns das Ganze noch ein paar Mal an.")
        # Zwei zusätzliche Runden
        for _ in range(2):
            self.play(theta.animate.set_value(0), run_time=0.5)
            self.play(theta.animate.set_value(TAU), run_time=4, rate_func=linear)

        set_subtitle("Der Punkt auf dem Einheitskreis bestimmt direkt Sinus und Cosinus des Winkels.")
        self.wait(2)

        # -------------------------------------------------------
        # AUSBLENDEN
        # -------------------------------------------------------
        self.play(
            FadeOut(
                left_group,
                graph_axes, x_label, y_label,
                sin_graph, cos_graph,
                moving_sin_dot, moving_cos_dot,
                sin_text, cos_text,
                sub, title
            )
        )
        self.wait(0.5)
