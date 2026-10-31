# caesar_narrated_v2.py
# Verbesserte Cäsar-Chiffre-Erklärszene – mehr Padding & höhere Position

from manim import *
import numpy as np
import string

SUBJECT = "Cäsar-Chiffre (Caesar Cipher)"

STEPS = [
    {"title": "Intro", "body": "• Was ist die Cäsar-Chiffre?\n• Monoalphabetische Substitution durch Verschieben des Alphabets\n• Parameter k: Anzahl der Schritte"},
    {"title": "Prinzip", "body": "• Wähle eine Verschiebung k (z. B. k = 3)\n• Jeder Buchstabe wird im Alphabet um k nach rechts verschoben\n• Z ‚wrappt‘ auf A zurück"},
    {"title": "Beispiel: Verschlüsseln", "body": "• Klartext: HALLO\n• k = 3 ⇒ H→K, A→D, L→O, L→O, O→R\n• Ergebnis: KHOOR"},
    {"title": "Entschlüsseln", "body": "• Rückverschiebung um k (oder Verschiebung um −k)\n• KHOOR → HALLO\n• Allgemein: Dec_k(C) = Enc_{26−k}(C)"},
    {"title": "Schwächen", "body": "• Nur 25 sinnvolle Schlüssel: Brute Force trivial\n• Häufigkeitsanalyse verrät Muster\n• Heute nur lehrreich, nicht sicher"},
    {"title": "Zusammenfassung", "body": "• Idee: Alphabet-Verschiebung mit Schlüssel k\n• Einfach zu verstehen – einfach zu brechen\n• Nächster Schritt: bessere Substitutionen"},
]


class SimpleNarrated(Scene):
    def construct(self):
        fw, fh = config.frame_width, config.frame_height
        panel_h = fh * 0.25
        panel_margin = 0.1
        pad_x, pad_y = 0.3, 0.2

        panel_bottom = -fh / 2 + panel_margin + panel_h * 0.15
        panel_y = panel_bottom + panel_h / 2
        panel_w = fw - 2 * panel_margin

        # --- Panel ---
        panel_color = GREY_E
        bg = Rectangle(width=panel_w, height=panel_h)
        bg.set_fill(panel_color, 1).set_stroke(opacity=0)
        bg.move_to([0, panel_y, 0])
        self.add(bg)

        # --- Title ---
        title = Text(SUBJECT, color=WHITE, weight=BOLD).scale(0.4)
        top_y = fh / 2 - 0.4
        title.move_to([0, top_y, 0])
        self.play(FadeIn(title, shift=0.3 * UP, run_time=0.6))

        # --- Placeholders ---
        headline = Text(".", color=panel_color).scale(0.25)
        body = Text(".", color=panel_color).scale(0.25)
        self.add(headline, body)

        # --- Visualization area ---
        viz_gap = 0.4  # etwas mehr Abstand nach unten
        viz_y = panel_y + panel_h / 2 + viz_gap + 1.6  # alles höher gesetzt

        def make_body(text):
            lines = []
            for raw in text.split("\n"):
                s = raw.strip()
                lines.append(f"• {s[2:]}" if s.startswith(("- ", "• ")) else raw)
            return Paragraph(*lines, alignment="left", line_spacing=0.7).scale(0.23)

        def update_panel(step_title, body_text):
            nonlocal headline, body
            new_h = Text(step_title, color=WHITE).scale(0.25)
            hx = -fw / 2 + panel_margin + pad_x + new_h.width / 2
            hy = panel_y + panel_h / 2 - pad_y - new_h.height / 2 - 0.1
            new_h.move_to([hx, hy, 0])

            new_b = make_body(body_text)
            new_b.set_max_width((panel_w - 2 * pad_x) * 0.9)
            bx = -fw / 2 + panel_margin + pad_x + new_b.width / 2
            by = new_h.get_bottom()[1] - 0.2 - new_b.height / 2
            min_y = panel_y - panel_h / 2 + pad_y
            if by - new_b.height / 2 < min_y:
                by = min_y + new_b.height / 2
            new_b.move_to([bx, by, 0])

            self.play(ReplacementTransform(headline, new_h, run_time=0.4))
            self.play(ReplacementTransform(body, new_b, run_time=0.4))
            headline, body = new_h, new_b

        # --- Caesar visuals ---
        letters = list(string.ascii_uppercase)

        def make_alphabet_row(y, label_text):
            label = Text(label_text).scale(0.3).move_to(np.array([-6.0, y, 0]))
            cells = VGroup()
            spacing = 0.52  # mehr Abstand zwischen Buchstaben
            start_x = -5.2
            for i, ch in enumerate(letters):
                t = Text(ch).scale(0.38)
                box = RoundedRectangle(corner_radius=0.08, width=0.46, height=0.55).set_stroke(GREY_C, 1)
                cell = VGroup(box, t)
                cell.move_to(np.array([start_x + i * spacing, y, 0]))
                cells.add(cell)
            return VGroup(label, cells)

        def label_at(group_cells, ch):
            idx = letters.index(ch)
            return group_cells[1][idx][1]

        row_plain = make_alphabet_row(viz_y, "Klartext:")
        row_cipher = make_alphabet_row(viz_y - 1.0, "Geheimtext:")
        k_value = 3
        k_text = MathTex("k = ", str(k_value)).scale(0.8)
        k_text.next_to(row_plain, UP, buff=0.25)

        arrows = VGroup()

        def set_cipher_row_for_k(k, animate=True, run_time=0.6):
            new_cells = []
            for i in range(26):
                ch = letters[(i + k) % 26]
                old_cell = row_cipher[1][i]
                new_t = Text(ch).scale(0.38).move_to(old_cell[1].get_center())
                new_cells.append(ReplacementTransform(old_cell[1], new_t))
                row_cipher[1][i][1] = new_t
            if animate:
                self.play(*new_cells, run_time=run_time)

        def add_mapping_arrows(chars, k):
            nonlocal arrows
            arrows_dest = VGroup()
            for ch in chars:
                i = letters.index(ch)
                j = (i + k) % 26
                start = row_plain[1][i].get_bottom() + 0.05 * DOWN
                end = row_cipher[1][j].get_top() + 0.05 * UP
                arr = Arrow(start, end, buff=0.08, stroke_width=2)
                arrows_dest.add(arr)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows_dest], lag_ratio=0.06, run_time=0.6))
            arrows = arrows_dest

        def clear_arrows():
            nonlocal arrows
            if len(arrows) > 0:
                self.play(FadeOut(arrows, run_time=0.3))
                arrows = VGroup()

        # --- Start visuals ---
        self.play(FadeIn(row_plain, shift=0.2 * UP, run_time=0.4))
        self.play(FadeIn(row_cipher, shift=0.2 * DOWN, run_time=0.4))
        self.play(FadeIn(k_text), run_time=0.3)
        set_cipher_row_for_k(k_value, animate=False)

        # --- Szenen ---
        update_panel(STEPS[0]["title"], STEPS[0]["body"])
        self.play(Indicate(row_plain[0]), Indicate(row_cipher[0]), run_time=0.6)

        update_panel(STEPS[1]["title"], STEPS[1]["body"])
        self.play(Indicate(k_text), run_time=0.5)
        clear_arrows()
        add_mapping_arrows(["A", "H", "Z"], k_value)
        self.play(Indicate(label_at(row_plain, "Z")), Indicate(label_at(row_cipher, "C")), run_time=0.5)

        update_panel(STEPS[2]["title"], STEPS[2]["body"])
        clear_arrows()

        def make_word_tiles(word, y):
            spacing = 0.65
            start_x = - (len(word) - 1) * spacing / 2
            tiles = VGroup()
            for i, ch in enumerate(word):
                t = Text(ch).scale(0.6)
                box = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.8).set_stroke(WHITE, 2)
                cell = VGroup(box, t).move_to(np.array([start_x + i * spacing, y, 0]))
                tiles.add(cell)
            return tiles

        word_plain = make_word_tiles("HALLO", row_plain.get_top()[1] + 1.2)
        word_cipher = make_word_tiles("KHOOR", row_cipher.get_bottom()[1] - 1.2)
        self.play(FadeIn(word_plain, shift=0.2 * DOWN), run_time=0.4)

        mapping_pairs = list(zip("HALLO", "KHOOR"))
        for p, c in mapping_pairs:
            self.play(Indicate(label_at(row_plain, p)), run_time=0.2)
            add_mapping_arrows([p], k_value)
            idx = [i for i, (pp, _) in enumerate(mapping_pairs) if pp == p][0]
            self.play(FadeIn(word_cipher[idx], shift=0.2 * UP), run_time=0.2)
            clear_arrows()
        self.wait(0.3)

        update_panel(STEPS[3]["title"], STEPS[3]["body"])
        self.play(Indicate(word_cipher), run_time=0.3)
        k_rev = (26 - k_value) % 26
        new_k = MathTex("k = ", str(k_rev), "\\ (entschl.)").scale(0.8)
        new_k.move_to(k_text.get_center())
        self.play(ReplacementTransform(k_text, new_k), run_time=0.4)
        set_cipher_row_for_k(k_rev, animate=True)
        clear_arrows()

        # Restore original k
        k_text = MathTex("k = ", str(k_value)).scale(0.8).move_to(new_k.get_center())
        self.play(ReplacementTransform(new_k, k_text), run_time=0.4)
        set_cipher_row_for_k(k_value, animate=True)

        update_panel(STEPS[4]["title"], STEPS[4]["body"])
        sample = "KHOOR"
        grid = VGroup()
        for i in range(5):
            dec = "".join(letters[(letters.index(ch) - i) % 26] for ch in sample)
            txt = Text(f"k={i}: {dec}").scale(0.3)
            txt.move_to(np.array([-4.8 + 2.4 * i, row_cipher.get_bottom()[1] - 1.0, 0]))
            grid.add(txt)
        self.play(FadeIn(grid), run_time=0.4)
        good = grid[3]
        box = SurroundingRectangle(good, color=YELLOW, buff=0.08)
        self.play(Create(box), run_time=0.3)
        self.play(Indicate(good), run_time=0.4)

        update_panel(STEPS[5]["title"], STEPS[5]["body"])
        self.play(*[FadeOut(m) for m in [word_plain, word_cipher, grid, box] if m is not None], run_time=0.4)
        self.play(Wiggle(row_plain[0]), Wiggle(row_cipher[0]), run_time=0.6)

        self.play(FadeOut(row_plain), FadeOut(row_cipher), FadeOut(k_text), run_time=0.5)


__all__ = ["SimpleNarrated"]
