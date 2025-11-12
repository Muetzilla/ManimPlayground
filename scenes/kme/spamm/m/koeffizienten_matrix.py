from manim import *

class MatrixTransformationLoop(Scene):
    def construct(self):
        def build_matrix(entries, buff_x=0.8, buff_y=0.4):
            rows = []
            for row in entries:
                tex_row = [MathTex(e) for e in row]
                row_group = VGroup(*tex_row).arrange(RIGHT, buff=buff_x)
                rows.append(row_group)
            return VGroup(*rows).arrange(DOWN, buff=buff_y)

        def create_augmented_matrix(left_data, right_data):
            left = build_matrix(left_data)
            right = build_matrix(right_data)

            height = max(left.height, right.height)
            divider = Line(UP * (height / 2), DOWN * (height / 2))
            matrix_core = VGroup(left, divider, right).arrange(RIGHT, buff=0.3)

            dummy = Matrix(
                [[0]],
                left_bracket="(",
                right_bracket=")"
                )
            left_bracket = dummy.get_brackets()[0].copy()
            right_bracket = dummy.get_brackets()[1].copy()

            left_bracket.stretch_to_fit_height(matrix_core.height + 0.2)
            right_bracket.stretch_to_fit_height(matrix_core.height + 0.2)
            left_bracket.next_to(matrix_core, LEFT, buff=0.1)
            right_bracket.next_to(matrix_core, RIGHT, buff=0.1)

            return VGroup(left_bracket, matrix_core, right_bracket)

        def flatten(matrix_data):
            return [item for row in matrix_data for item in row]

        def get_entries_from_matrix_group(matrix_group):
            left_matrix = matrix_group[1][0]
            right_matrix = matrix_group[1][2]
            entries = []
            for row in left_matrix:
                entries += list(row)
            for row in right_matrix:
                entries += list(row)
            return entries

        def highlight_changes(prev_left, prev_right, new_matrix_group):
            prev_flat = flatten(prev_left + prev_right)
            new_entries = get_entries_from_matrix_group(new_matrix_group)
            for prev_val, new_tex in zip(prev_flat, new_entries):
                if new_tex.get_tex_string() != prev_val:
                    new_tex.set_color(BLUE)

        # Schritte definiern
        steps = [
            {
                "left": [
                    ["6", "8", "3"],
                    ["4", "7", "3"],
                    ["1", "2", "1"]
                ],
                "right": [
                    ["1", "0", "0"],
                    ["0", "1", "0"],
                    ["0", "0", "1"]
                ],
                "annotations": [r"\div 6", r"\div 4", r"- \mathrm{I}"],
                "caption": "Starte mit der erweiterten Koeffizientenmatrix"
            },
            {
                "left": [
                    ["1", r"\dfrac{4}{3}", r"\dfrac{1}{2}"],
                    ["1", r"\dfrac{7}{4}", r"\dfrac{3}{4}"],
                    ["1", "2", "1"]
                ],
                "right": [
                    [r"\dfrac{1}{6}", "0", "0"],
                    ["0", r"\dfrac{1}{4}", "0"],
                    ["0", "0", "1"]
                ],
                "annotations": [r"R_2 - R_1", r"R_3 - R_1"],
                "caption": "Normiere die erste Zeile"
            },
            {
                "left": [
                    ["1", r"\dfrac{4}{3}", r"\dfrac{1}{2}"],
                    ["0", r"\dfrac{1}{12}", r"\dfrac{1}{4}"],
                    ["0", r"\dfrac{2}{3}", r"\dfrac{1}{2}"]
                ],
                "right": [
                    [r"\dfrac{1}{6}", "0", "0"],
                    [r"-\dfrac{1}{6}", r"\dfrac{1}{4}", "0"],
                    [r"-\dfrac{1}{6}", "0", "1"]
                ],
                "annotations": [r"R_2 - R_1", r"R_3 - R_1"],
                "caption": "Eliminiere erste Spalte unten"
            }
        ]

        # Titel oben
        title = Tex("Gaußsches Eliminationsverfahren").scale(0.9).to_edge(UP)
        self.play(Write(title))

        # Startmatrix + Caption unten
        current_matrix = create_augmented_matrix(steps[0]["left"], steps[0]["right"])
        self.play(Write(current_matrix))

        # Zeilenbeschriftungen
        row_labels = [
            MathTex(r"\mathrm{I}").shift(UP * 0.6),
            MathTex(r"\mathrm{II}").shift(UP * 0.1),
            MathTex(r"\mathrm{III}").shift(DOWN * 0.6)
        ]
        for label in row_labels:
            label.next_to(current_matrix, LEFT)
        #self.play(*[Write(lbl) for lbl in row_labels])

        # Caption unten
        caption = Tex(steps[0]["caption"]).scale(0.7).next_to(current_matrix, DOWN, buff=0.7)
        self.play(Write(caption))

        # Schleife durch Schritte
        prev_left = steps[0]["left"]
        prev_right = steps[0]["right"]

        for i in range(1, len(steps)):
            step = steps[i]
            next_matrix = create_augmented_matrix(step["left"], step["right"])
            highlight_changes(prev_left, prev_right, next_matrix)

            # Neue Caption
            new_caption = Tex(step["caption"]).scale(0.7).next_to(current_matrix, DOWN, buff=0.7)

            # Annotationen
            annotations = [
                MathTex(text).scale(0.7).next_to(current_matrix, RIGHT).shift(UP * (0.6 - 0.5 * j))
                for j, text in enumerate(step["annotations"])
            ]
            self.play(*[Write(a) for a in annotations])
            self.wait(0.5)

            # Farben zurück auf Weiß VOR dem Übergang
            for entry in get_entries_from_matrix_group(current_matrix):
                entry.set_color(WHITE)

            # Matrix + Caption aktualisieren
            self.play( *[FadeOut(a) for a in annotations], Transform(current_matrix, next_matrix), Transform(caption, new_caption))


            prev_left = step["left"]
            prev_right = step["right"]

        self.wait(2)
