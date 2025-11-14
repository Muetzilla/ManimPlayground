from manim import *

class CaesarCipherScene(Scene):
    # --- Einstellungen (einfach anpassen) ---
    SHIFT = 3
    PLAINTEXT = "HALLO WELT"

    # Ränder (zum Frame)
    LEFT_MARGIN = 0.8
    RIGHT_MARGIN = 0.8
    TOP_MARGIN = 0.7
    BOTTOM_MARGIN = 0.7

    # Schriftgrößen
    TITLE_FS = 52
    ABC_FS = 30
    PAIR_FS = 42
    STATUS_LABEL_FS = 30
    STATUS_VAL_FS = 34
    SUBTITLE_FS = 28

    # Abstände
    GAP_AFTER_TITLE = 0.6
    GAP_AFTER_ABC = 0.8
    GAP_AFTER_PAIRS = 0.8
    GAP_PAIRS = 0.5          # Abstand zwischen H→K, …
    GAP_PAIR_LINES = 0.9     # vertikaler Abstand zwischen Paarzeilen
    ABC_ROW_GAP = 0.35       # Abstand Original <-> Verschoben
    PANEL_PAD_X = 0.5
    PANEL_PAD_Y = 0.28

    # Panel-Opazitäten
    ABC_BG_OPACITY = 0.10
    STATUS_BG_OPACITY = 0.10
    SUBTITLE_BG_OPACITY = 0.12

    def construct(self):
        # Farben
        COL_A = YELLOW
        COL_S = BLUE
        COL_P = GREEN
        COL_C = RED

        # Hilfsfunktionen
        def caesar_shift(ch, k=self.SHIFT):
            if ch == " ":
                return " "
            return chr((ord(ch) - 65 + k) % 26 + 65)

        def make_row(chars, color, fs):
            g = VGroup(*[Text(ch, font_size=fs, color=color) for ch in chars])
            g.arrange(RIGHT, buff=0.22)
            return g

        def panel(mobj, pad_x=self.PANEL_PAD_X, pad_y=self.PANEL_PAD_Y, stroke=1, fill_opacity=0.1):
            r = Rectangle(width=mobj.width + 2*pad_x, height=mobj.height + 2*pad_y)\
                    .set_stroke(WHITE, stroke).set_fill(opacity=fill_opacity)
            r.move_to(mobj)
            return VGroup(r, mobj)

        # verfügbare Breite (mit Rändern)
        avail_w = config.frame_width - self.LEFT_MARGIN - self.RIGHT_MARGIN

        # --- Titel ---
        title = Text(f"Cäsar-Chiffre (Shift = {self.SHIFT})", font_size=self.TITLE_FS)
        title.to_edge(UP, buff=self.TOP_MARGIN)
        self.play(FadeIn(title, shift=UP*0.2))

        # --- Alphabet (vollbreit, ggf. skalieren) ---
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        shifted = [letters[(i + self.SHIFT) % 26] for i in range(26)]
        row_orig  = make_row(letters, COL_A, self.ABC_FS)
        row_shift = make_row(shifted, COL_S, self.ABC_FS)

        labels = VGroup(
            Text("Original", font_size=20, color=COL_A),
            Text(f"Verschoben um {self.SHIFT}", font_size=20, color=COL_S),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.16)

        alphabets = VGroup(
            labels,
            VGroup(row_orig, row_shift).arrange(DOWN, buff=self.ABC_ROW_GAP)
        ).arrange(RIGHT, buff=0.5)

        # Skaliere Alphabet-Block, falls zu breit
        if alphabets.width > avail_w:
            alphabets.scale_to_fit_width(avail_w)

        alphabets.next_to(title, DOWN, buff=self.GAP_AFTER_TITLE)
        alphabets.to_edge(LEFT, buff=self.LEFT_MARGIN)
        abc_panel = panel(alphabets, fill_opacity=self.ABC_BG_OPACITY)
        self.play(FadeIn(abc_panel))

        # --- Paare (H→K, …) unter Alphabet – mit automatischem Umbruch ---
        # Container, der in Zeilen füllt bis avail_w, zentriert
        pairs_container = VGroup()
        current_line = VGroup()

        plaintext = self.PLAINTEXT
        # Vorschub-Anker (Position unter dem ABC-Panel)
        start_y = abc_panel.get_bottom()[1] - self.GAP_AFTER_ABC

        def flush_line(line, line_index):
            if len(line) == 0:
                return
            line.arrange(RIGHT, buff=self.GAP_PAIRS)
            # Zentriere die Zeile innerhalb der verfügbaren Breite
            line.move_to(np.array([0, start_y - line_index * self.GAP_PAIR_LINES, 0]))
            pairs_container.add(line)

        for ch in plaintext:
            pair = VGroup(
                Text(ch, font_size=self.PAIR_FS, color=COL_P),
                Text("→", font_size=int(self.PAIR_FS*0.82)),
                Text(caesar_shift(ch), font_size=self.PAIR_FS, color=COL_C),
            ).arrange(RIGHT, buff=0.2)

            # Passt es noch in die aktuelle Zeile?
            test = VGroup(*current_line, pair).arrange(RIGHT, buff=self.GAP_PAIRS)
            if test.width > avail_w and len(current_line) > 0:
                # alte Zeile abschließen und neue Zeile beginnen
                flush_line(current_line, len(pairs_container))
                current_line = VGroup(pair)
            else:
                current_line.add(pair)

            # animiere Anzeige (Highlight im Alphabet)
            if ch != " ":
                idx = ord(ch) - 65
                box_plain = Rectangle(width=row_orig[idx].width+0.12, height=row_orig[idx].height+0.12)\
                                .set_stroke(COL_P, 3).move_to(row_orig[idx])
                box_shift = Rectangle(width=row_shift[idx].width+0.12, height=row_shift[idx].height+0.12)\
                                .set_stroke(COL_C, 3).move_to(row_shift[idx])
                self.play(Create(box_plain), Create(box_shift), run_time=0.3)
                self.play(FadeIn(pair, scale=0.75), run_time=0.3)
                self.play(FadeOut(box_plain), FadeOut(box_shift), run_time=0.25)
            else:
                self.play(FadeIn(pair, scale=0.75), run_time=0.25)

        # letzte Zeile flushen
        flush_line(current_line, len(pairs_container))
        self.add(pairs_container)

        # --- Status (unter den Paaren, zentriert – keine Überlappung möglich) ---
        status_lbl_ct = Text("Klartext:", font_size=self.STATUS_LABEL_FS, color=COL_P)
        status_val_ct = Text(self.PLAINTEXT, font_size=self.STATUS_VAL_FS, color=COL_P)
        status_lbl_cc = Text("Geheimtext:", font_size=self.STATUS_LABEL_FS, color=COL_C)
        status_val_cc = Text("", font_size=self.STATUS_VAL_FS, color=COL_C)

        status_block = VGroup(
            VGroup(status_lbl_ct, status_val_ct).arrange(RIGHT, buff=0.35),
            VGroup(status_lbl_cc, status_val_cc).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        # skaliere Statuspanel, falls breiter als avail_w
        if status_block.width > avail_w:
            status_block.scale_to_fit_width(avail_w)

        status_panel = panel(status_block, fill_opacity=self.STATUS_BG_OPACITY)
        status_panel.next_to(pairs_container, DOWN, buff=self.GAP_AFTER_PAIRS)
        # zentrieren
        status_panel.move_to(np.array([0, status_panel.get_center()[1], 0]))
        self.play(FadeIn(status_panel), run_time=0.3)

        # --- Untertitel-Leiste (am unteren Rand, mit Padding) ---
        subtitle_box = Rectangle(width=avail_w, height=1.6).set_stroke(WHITE, 2).set_fill(opacity=self.SUBTITLE_BG_OPACITY)
        subtitle_box.to_edge(DOWN, buff=self.BOTTOM_MARGIN)
        subtitle = Text("Die Cäsar-Chiffre verschiebt jeden Buchstaben um eine feste Anzahl.", font_size=self.SUBTITLE_FS)\
                    .move_to(subtitle_box.get_center())
        self.play(FadeIn(subtitle_box), Write(subtitle), run_time=0.3)

        def set_subtitle(msg):
            self.play(Transform(subtitle, Text(msg, font_size=self.SUBTITLE_FS).move_to(subtitle_box.get_center())), run_time=0.25)

        # --- Geheimtext live aufbauen (ohne Überlagerung) ---
        cipher_so_far = ""
        for ch in plaintext:
            cipher_so_far += caesar_shift(ch)
            new_val = Text(cipher_so_far, font_size=self.STATUS_VAL_FS, color=COL_C)
            new_val.move_to(status_val_cc.get_center())
            self.play(Transform(status_val_cc, new_val), run_time=0.2)
            if ch != " ":
                set_subtitle(f"'{ch}' wird um {self.SHIFT} verschoben und zu '{caesar_shift(ch)}'.")
            else:
                set_subtitle("Leerzeichen bleiben Leerzeichen.")

        # Abschlussrahmen um finalen Geheimtext
        final_box = Rectangle(width=status_val_cc.width+0.22, height=status_val_cc.height+0.22)\
                        .set_stroke(COL_C, 3).move_to(status_val_cc)
        self.play(Create(final_box), run_time=0.25)
        set_subtitle(f"Fertig! '{self.PLAINTEXT}' → '{cipher_so_far}'.")
        self.wait(1.8)
