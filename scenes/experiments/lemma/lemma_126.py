from manimlib.imports import *

MathTex = TexMobject
Circumscribe = Indicate

BLUE = BLUE_C
GREEN = GREEN_C
RED = RED_C
GOLD = YELLOW
WHITE_TEXT = "#F4F6F7"


class VektorAustausch(Scene):

    def make_card(self, symbol, color):
        box = RoundedRectangle(
            width=1.55,
            height=1.25,
            corner_radius=0.16,
            stroke_width=3,
        )
        box.set_stroke(color, width=3, opacity=1)
        box.set_fill(color, opacity=0.18)

        label = MathTex(
            symbol,
            font_size=43,
        )
        label.set_color(WHITE)

        label.move_to(box)

        return VGroup(box, label)

    def positions(self, count):
        spacing = 1.9
        return [
            RIGHT * ((i - (count - 1) / 2) * spacing)
            for i in range(count)
        ]

    def lower_positions(self, count):
        return [position + DOWN * 1.7 for position in self.positions(count)]

    def construct(self):
        self.camera.background_color = "#101827"

        title = Text(
            "Der Austausch von Vektoren",
            font_size=38,
            weight=BOLD,
        ).to_edge(UP)

        hint = Text(
            "Gruene v_i ersetzen blaue e_i | Blaue e_i: Ausgangsbasis",
            font_size=20,
            color=WHITE,
        ).next_to(title, DOWN, buff=0.18)

        subtitle = MathTex(
            r"\operatorname{Span}"
            r"(\mathbf e_1,\ldots,\mathbf e_4)"
            r"=\mathbb R^4",
            font_size=37,
        ).to_edge(DOWN, buff=0.7)

        result_frame = Rectangle(
            width=8.4,
            height=0.9,
            color=GREEN,
            stroke_width=2,
        ).move_to(subtitle)
        result_frame.set_fill(opacity=0)

        basis_frame = Rectangle(
            width=8.8,
            height=1.45,
            color=BLUE,
            stroke_width=2,
        ).shift(DOWN * 1.7)
        basis_frame.set_fill(opacity=0)

        self.play(Write(title), FadeIn(hint))
        self.play(
            ShowCreation(result_frame),
            Write(subtitle),
        )

        span_frame = Rectangle(
            width=9.6,
            height=1.75,
            color=GOLD,
            stroke_width=2,
        )
        span_frame.set_fill(opacity=0)
        span_label = Text(
            "Span",
            font_size=24,
            color=GOLD,
        ).next_to(span_frame, UP, buff=0.08)

        self.play(
            ShowCreation(span_frame),
            FadeIn(span_label),
            ShowCreation(basis_frame),
            run_time=0.8,
        )

        # Anfang: vier Einheitsvektoren
        cards = [
            self.make_card(r"\mathbf e_1", BLUE),
            self.make_card(r"\mathbf e_2", BLUE),
            self.make_card(r"\mathbf e_3", BLUE),
            self.make_card(r"\mathbf e_4", BLUE),
        ]

        for card, pos in zip(cards, self.positions(4)):
            card.move_to(pos)

        basis_cards = [
            self.make_card(r"\mathbf e_1", BLUE),
            self.make_card(r"\mathbf e_2", BLUE),
            self.make_card(r"\mathbf e_3", BLUE),
            self.make_card(r"\mathbf e_4", BLUE),
        ]

        for card, pos in zip(basis_cards, self.lower_positions(4)):
            card.move_to(pos)

        self.add(*cards, *basis_cards)
        self.play(
            *[
                ApplyMethod(card.shift, UP * 0.4)
                for card in cards + basis_cards
            ],
            run_time=0.8,
        )
        self.play(
            *[
                ApplyMethod(card.shift, DOWN * 0.4)
                for card in cards + basis_cards
            ],
            run_time=0.5,
        )

        self.wait(1)

        for k in range(1, 5):

            # Neuer Vektor kommt von ausserhalb des Span-Rahmens.
            replacement_card = self.make_card(
                rf"\mathbf v_{k}",
                GREEN
            )

            insert_index = k - 1

            positions5 = self.positions(5)
            replacement_card.move_to(
                self.lower_positions(4)[insert_index]
            )

            new_cards = cards.copy()
            new_cards.insert(insert_index, replacement_card)

            # Platz schaffen und den neuen Vektor sichtbar einschieben.
            removed = new_cards[k]

            self.add(replacement_card)

            self.play(
                *[
                    ApplyMethod(
                        card.move_to,
                        pos
                    )
                    for card, pos in zip(new_cards, positions5)
                ],
                run_time=1.8,
            )

            self.play(
                Indicate(replacement_card, color=GREEN),
                run_time=0.5,
            )

            self.wait(0.5)

            self.play(
                ApplyMethod(removed[0].set_stroke, RED, width=5),
                ApplyMethod(removed[1].set_color, RED),
            )

            self.wait(1.2)

            # Der ersetzte Einheitsvektor gleitet aus dem Span heraus.
            new_cards.pop(k)
            self.play(
                ApplyMethod(removed.shift, DOWN * 1.0),
                *[
                    ApplyMethod(card.move_to, pos)
                    for card, pos in zip(
                        new_cards,
                        self.positions(4)
                    )
                ],
                run_time=1.4,
            )

            self.play(
                FadeOut(removed, scale=0.6),
                run_time=0.6,
            )

            cards = new_cards

            # Der Spann bleibt unverändert
            self.play(
                Indicate(
                    subtitle,
                    color=GREEN,
                    scale_factor=1.05,
                ),
                run_time=0.8,
            )

            self.wait(0.5)

        # Abschluss
        self.add(*cards)
        self.add(*basis_cards)
        self.play(
            *[
                ApplyMethod(card.move_to, pos)
                for card, pos in zip(
                    cards,
                    self.positions(4)
                )
            ],
            *[
                ApplyMethod(card.move_to, pos)
                for card, pos in zip(
                    basis_cards,
                    self.lower_positions(4)
                )
            ],
            run_time=0.8,
        )

        final_text = MathTex(
            r"\operatorname{Span}"
            r"(\mathbf v_1,\mathbf v_2,"
            r"\mathbf v_3,\mathbf v_4)"
            r"=\mathbb R^4",
            font_size=39,
            color=GREEN,
        ).to_edge(DOWN, buff=0.7)

        self.play(
            ReplacementTransform(
                subtitle,
                final_text
            )
        )

        self.play(
            Circumscribe(
                VGroup(*cards),
                color=GOLD,
                run_time=2,
            )
        )

        self.wait(3)