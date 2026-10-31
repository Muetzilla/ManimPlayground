"""
Die Cäsar-Chiffre – Erklärvideo mit Manim (Community Edition)

Rendern:
    manim -pqh caesar_chiffre.py CaesarChiffre      # 1080p60, Vorschau
    manim -pql caesar_chiffre.py CaesarChiffre      # schnelle Testvorschau (480p)
    manim -pqk caesar_chiffre.py CaesarChiffre      # 4K

Layout-Regeln, damit sich nichts überlagert:
  * Jede Szene beginnt mit einem leeren Bildschirm (clear()).
  * Titel stehen immer oben (y ≈ 3.25), Inhalt darunter, feste Zonen:
        y 2.45  Beschriftung Klartext-Alphabet
        y 1.80  Klartext-Alphabet
        y 0.30  Geheimtext-Alphabet
        y -0.35 Beschriftung Geheimtext-Alphabet
        y -1.50 Wort (Quelle)      y -2.90 Wort (Ergebnis)
  * Texte, die sich ändern, werden per ReplacementTransform ersetzt,
    nie einfach darübergeschrieben.
"""
from manim import *
import numpy as np

# --------------------------------------------------------------------------
# Design
# --------------------------------------------------------------------------
BG = "#10131f"
PLAIN = BLUE_C        # Klartext
CIPHER = YELLOW       # Geheimtext
OK = GREEN_C
MUTED = GRAY_B

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SHIFT = 3
CELL = 0.46           # Kantenlänge einer Alphabet-Zelle
STEP = 0.51           # Abstand von Zelle zu Zelle


# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------
def caesar(text, k):
    out = ""
    for ch in text:
        if ch.isalpha():
            out += chr((ord(ch) - 65 + k) % 26 + 65)
        else:
            out += ch
    return out


def fit(mob, width=12.8):
    """Skaliert ein Objekt runter, falls es breiter als der sichere Bereich ist."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def make_cell(ch, color, side=CELL, fs=22):
    sq = Square(
        side_length=side,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.12,
    )
    tx = Text(ch, font_size=fs, color=WHITE).move_to(sq.get_center())
    return VGroup(sq, tx)


def make_row(letters, color):
    row = VGroup(*[make_cell(ch, color) for ch in letters])
    row.arrange(RIGHT, buff=STEP - CELL)
    return row


def hl(cell, color):
    return cell[0].animate.set_fill(color, opacity=0.6)


def unhl(cell, color):
    return cell[0].animate.set_fill(color, opacity=0.12)


# --------------------------------------------------------------------------
# Die Szene
# --------------------------------------------------------------------------
class CaesarChiffre(Scene):
    # ---------- allgemeine Helfer ----------
    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.2)

    def make_head(self, text):
        t = Text(text, font_size=42, weight=BOLD, color=WHITE)
        fit(t, 12.5)
        t.to_edge(UP, buff=0.45)
        ul = Line(LEFT, RIGHT, color=PLAIN, stroke_width=3)
        ul.set_width(t.width + 0.6).next_to(t, DOWN, buff=0.12)
        return VGroup(t, ul)

    def show_title(self, text):
        head = self.make_head(text)
        self.play(Write(head[0]), Create(head[1]), run_time=1.2)
        return head

    def swap_title(self, old_head, text):
        new_head = self.make_head(text)
        self.play(ReplacementTransform(old_head, new_head), run_time=1.0)
        return new_head

    # ---------- Ablauf ----------
    def construct(self):
        self.camera.background_color = BG
        self.intro()
        self.idea()
        self.alphabet_and_encrypt()
        self.modular_arithmetic()
        self.decrypt()
        self.brute_force()
        self.frequency_analysis()
        self.outro()

    # ---------- 1. Intro ----------
    def intro(self):
        title = Text("Die Cäsar-Chiffre", font_size=72, weight=BOLD)
        line = Line(LEFT, RIGHT, color=PLAIN, stroke_width=4).set_width(title.width + 1)
        title.move_to([0, 0.5, 0])
        line.next_to(title, DOWN, buff=0.25)
        sub = Text("Wie die Römer Nachrichten versteckten", font_size=34, color=MUTED)
        sub.next_to(line, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.6)
        self.play(Create(line), run_time=0.8)
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=1.0)
        self.wait(1.5)
        self.clear()

    # ---------- 2. Die Idee ----------
    def idea(self):
        head = self.show_title("Die Idee")

        lab1 = Text("Nachricht (Klartext)", font_size=26, color=PLAIN)
        lab1.move_to([0, 2.0, 0])
        msg = Text("VENI VIDI VICI", font_size=54, color=WHITE).move_to([0, 1.2, 0])

        arrow = Arrow([0, 0.55, 0], [0, -0.35, 0], buff=0, color=MUTED, stroke_width=5)
        shift_lbl = Text("jeder Buchstabe + 3", font_size=26, color=MUTED)
        shift_lbl.move_to([2.7, 0.1, 0])

        lab2 = Text("Geheimtext", font_size=26, color=CIPHER).move_to([0, -0.9, 0])
        enc = Text(caesar("VENI VIDI VICI", SHIFT), font_size=54, color=CIPHER)
        enc.move_to([0, -1.8, 0])

        note = Text(
            "Cäsar soll so Briefe an seine Generäle geschützt haben.",
            font_size=26,
            color=MUTED,
        ).move_to([0, -3.2, 0])
        fit(note)

        self.play(FadeIn(lab1), Write(msg), run_time=1.5)
        self.wait(0.5)
        self.play(GrowArrow(arrow), FadeIn(shift_lbl), run_time=1.0)
        self.play(FadeIn(lab2), run_time=0.5)
        # Buchstabe für Buchstabe verwandeln (gleiche Position, nichts liegt doppelt)
        self.play(
            TransformFromCopy(msg, enc),
            run_time=2.0,
        )
        self.wait(0.8)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2.0)
        self.clear()

    # ---------- 3. + 4. Alphabet verschieben und verschlüsseln ----------
    def alphabet_and_encrypt(self):
        head = self.show_title("Das Prinzip: Alphabet verschieben")

        top = make_row(ALPHA, PLAIN).move_to([0, 1.8, 0])
        bottom = make_row(ALPHA, CIPHER).move_to([0, 0.3, 0])
        xs = [c.get_center()[0] for c in bottom]
        left_x = top.get_left()[0]

        lbl_top = Text("Klartext-Alphabet", font_size=22, color=PLAIN)
        lbl_top.move_to([left_x, 2.45, 0], aligned_edge=LEFT)
        lbl_bot = Text("Geheimtext-Alphabet", font_size=22, color=CIPHER)
        lbl_bot.move_to([left_x, -0.35, 0], aligned_edge=LEFT)

        self.play(
            FadeIn(lbl_top),
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in top], lag_ratio=0.04),
            run_time=2.0,
        )
        self.play(
            FadeIn(lbl_bot),
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in bottom], lag_ratio=0.04),
            run_time=2.0,
        )
        self.wait(0.8)

        # --- Verschiebung um 3 Stellen ---
        lbl_bot2 = Text("Geheimtext-Alphabet (um 3 verschoben)", font_size=22, color=CIPHER)
        lbl_bot2.move_to([left_x, -0.35, 0], aligned_edge=LEFT)

        first = VGroup(*bottom[:SHIFT])      # A, B, C – wandern ans Ende
        rest = VGroup(*bottom[SHIFT:])       # D … Z – rücken nach links
        # 1) A, B, C heben sich aus der Reihe, der Rest rutscht nach links
        self.play(
            first.animate.shift(UP * 0.75),
            rest.animate.shift(LEFT * SHIFT * STEP),
            ReplacementTransform(lbl_bot, lbl_bot2),
            run_time=2.0,
        )
        # 2) A, B, C fahren (oberhalb der Reihe) ans rechte Ende
        self.play(
            *[
                first[j].animate.set_x(xs[26 - SHIFT + j])
                for j in range(SHIFT)
            ],
            run_time=1.8,
        )
        # 3) und setzen sich wieder in die Reihe
        self.play(first.animate.shift(DOWN * 0.75), run_time=0.8)
        self.wait(0.6)

        def cipher_cell(c):
            """Zelle des Geheimtext-Alphabets, die unter Klartext-Spalte c steht."""
            return bottom[(c + SHIFT) % 26]

        # --- Beispiele für die Zuordnung ---
        map1 = Text("A → D", font_size=36, color=WHITE).move_to([3.5, -0.35, 0])
        self.play(hl(top[0], PLAIN), hl(cipher_cell(0), CIPHER), FadeIn(map1), run_time=0.8)
        self.wait(1.2)

        map2 = Text("X → A", font_size=36, color=WHITE).move_to([3.5, -0.35, 0])
        self.play(
            unhl(top[0], PLAIN),
            unhl(cipher_cell(0), CIPHER),
            hl(top[23], PLAIN),
            hl(cipher_cell(23), CIPHER),
            ReplacementTransform(map1, map2),
            run_time=0.9,
        )
        self.wait(1.4)
        self.play(unhl(top[23], PLAIN), unhl(cipher_cell(23), CIPHER), FadeOut(map2), run_time=0.6)

        # --- Wort verschlüsseln ---
        head = self.swap_title(head, "Verschlüsseln: HALLO")
        word = "HALLO"
        self.animate_word(
            src_word=word,
            dst_word=caesar(word, SHIFT),
            cols=[ord(ch) - 65 for ch in word],
            src_fn=lambda c: top[c],
            dst_fn=cipher_cell,
            src_label="Klartext:",
            dst_label="Geheimtext:",
            src_color=PLAIN,
            dst_color=CIPHER,
        )
        self.wait(2.0)
        self.clear()

    def animate_word(
        self, src_word, dst_word, cols, src_fn, dst_fn,
        src_label, dst_label, src_color, dst_color,
        y_src=-1.5, y_dst=-2.9,
    ):
        n = len(src_word)
        wstep = 0.8
        x0 = -1.0 - (n - 1) * wstep / 2
        xs_w = [x0 + j * wstep for j in range(n)]

        lab_s = Text(src_label, font_size=28, color=src_color)
        lab_s.move_to([-6.6, y_src, 0], aligned_edge=LEFT)
        lab_d = Text(dst_label, font_size=28, color=dst_color)
        lab_d.move_to([-6.6, y_dst, 0], aligned_edge=LEFT)

        src_cells = VGroup(
            *[
                make_cell(ch, src_color, 0.62, 32).move_to([xs_w[j], y_src, 0])
                for j, ch in enumerate(src_word)
            ]
        )
        slots = VGroup(
            *[
                Square(0.62, stroke_color=GRAY, stroke_width=2, stroke_opacity=0.5)
                .move_to([xs_w[j], y_dst, 0])
                for j in range(n)
            ]
        )
        self.play(
            FadeIn(lab_s),
            LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in src_cells], lag_ratio=0.15),
            run_time=1.2,
        )
        self.play(FadeIn(lab_d), Create(slots), run_time=0.8)
        self.wait(0.4)

        for j in range(n):
            a = src_fn(cols[j])
            b = dst_fn(cols[j])
            new = make_cell(dst_word[j], dst_color, 0.62, 32).move_to([xs_w[j], y_dst, 0])
            self.play(
                hl(src_cells[j], src_color),
                hl(a, src_color),
                hl(b, dst_color),
                run_time=0.6,
            )
            self.play(TransformFromCopy(b, new), FadeOut(slots[j]), run_time=0.9)
            self.play(
                unhl(src_cells[j], src_color),
                unhl(a, src_color),
                unhl(b, dst_color),
                run_time=0.4,
            )

    # ---------- 5. Rechnen mit Rest ----------
    def modular_arithmetic(self):
        head = self.show_title("Der Trick: Rechnen mit Rest")

        c = np.array([-3.4, -0.4, 0])

        def pos(idx, r):
            a = PI / 2 - TAU * idx / 26
            return c + r * np.array([np.cos(a), np.sin(a), 0])

        guide = Circle(radius=2.17, color=GRAY, stroke_width=1.5, stroke_opacity=0.5)
        guide.move_to(c)

        outer = VGroup(
            *[Text(ch, font_size=24, color=PLAIN).move_to(pos(i, 2.5)) for i, ch in enumerate(ALPHA)]
        )
        off = ValueTracker(0)
        inner = VGroup(*[Text(ch, font_size=22, color=CIPHER) for ch in ALPHA])
        for i, t in enumerate(inner):
            t.move_to(pos(i, 1.85))
            t.add_updater(lambda m, i=i: m.move_to(pos(i + off.get_value(), 1.85)))

        legend = VGroup(
            Text("außen: Klartext", font_size=20, color=PLAIN),
            Text("innen: Geheimtext", font_size=20, color=CIPHER),
        ).arrange(DOWN, buff=0.15).move_to(c)

        self.play(Create(guide), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in outer], lag_ratio=0.03), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(t) for t in inner], lag_ratio=0.03), run_time=1.6)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(0.6)

        # inneren Ring um 3 Stellen drehen
        self.play(off.animate.set_value(-SHIFT), run_time=3.0, rate_func=smooth)
        self.remove(off)
        self.wait(0.5)

        # Text-Panel rechts (alle Zeilen vorab angeordnet -> keine Überlagerung)
        lines = VGroup(
            Text("Nach Z geht's wieder bei A los.", font_size=28, color=WHITE),
            Text("Als Formel:", font_size=26, color=MUTED),
            Text("E(x) = (x + k) mod 26", font_size=32, color=CIPHER),
            Text("D(y) = (y − k) mod 26", font_size=32, color=PLAIN),
            Text("Beispiel: X = 23", font_size=26, color=MUTED),
            Text("(23 + 3) mod 26 = 0 = A", font_size=30, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(lines, 5.8)
        lines.move_to([0.9, -0.2, 0], aligned_edge=LEFT)

        # Wrap-around hervorheben: X, Y, Z (außen) und A, B, C (innen)
        wrap = [outer[i] for i in (23, 24, 25)] + [inner[i] for i in (0, 1, 2)]
        self.play(
            *[m.animate.set_color(OK).scale(1.35) for m in wrap],
            Write(lines[0]),
            run_time=1.5,
        )
        self.wait(1.5)
        self.play(
            *[m.animate.set_color(PLAIN if m in outer else CIPHER).scale(1 / 1.35) for m in wrap],
            run_time=0.8,
        )
        self.play(FadeIn(lines[1], shift=RIGHT * 0.2), run_time=0.6)
        self.play(Write(lines[2]), run_time=1.4)
        self.wait(0.6)
        self.play(Write(lines[3]), run_time=1.4)
        self.wait(1.0)
        self.play(FadeIn(lines[4], shift=RIGHT * 0.2), run_time=0.6)
        self.play(Write(lines[5]), run_time=1.6)
        self.wait(2.5)
        self.clear()

    # ---------- 6. Entschlüsseln ----------
    def decrypt(self):
        head = self.show_title("Entschlüsseln: einfach rückwärts")

        shifted = [ALPHA[(i + SHIFT) % 26] for i in range(26)]
        top = make_row(ALPHA, PLAIN).move_to([0, 1.8, 0])
        bottom = make_row(shifted, CIPHER).move_to([0, 0.3, 0])
        left_x = top.get_left()[0]

        lbl_top = Text("Klartext-Alphabet", font_size=22, color=PLAIN)
        lbl_top.move_to([left_x, 2.45, 0], aligned_edge=LEFT)
        lbl_bot = Text("Geheimtext-Alphabet (um 3 verschoben)", font_size=22, color=CIPHER)
        lbl_bot.move_to([left_x, -0.35, 0], aligned_edge=LEFT)

        self.play(
            FadeIn(lbl_top),
            FadeIn(lbl_bot),
            LaggedStart(*[FadeIn(c) for c in top], lag_ratio=0.02),
            LaggedStart(*[FadeIn(c) for c in bottom], lag_ratio=0.02),
            run_time=2.0,
        )
        self.wait(0.6)

        plain_word = "HALLO"
        cipher_word = caesar(plain_word, SHIFT)
        self.animate_word(
            src_word=cipher_word,
            dst_word=plain_word,
            cols=[ord(ch) - 65 for ch in plain_word],
            src_fn=lambda col: bottom[col],      # Spalte col des Geheimtext-Alphabets
            dst_fn=lambda col: top[col],
            src_label="Geheimtext:",
            dst_label="Klartext:",
            src_color=CIPHER,
            dst_color=PLAIN,
        )
        self.wait(2.0)
        self.clear()

    # ---------- 7. Brute Force ----------
    def brute_force(self):
        head = self.show_title("Schwachstelle 1: Alles ausprobieren")

        cipher = caesar("HALLO WELT", SHIFT)   # KDOOR ZHOW

        lab = Text("Abgefangener Geheimtext", font_size=26, color=CIPHER).move_to([0, 1.8, 0])
        ct = Text(cipher, font_size=56, color=CIPHER).move_to([0, 1.0, 0])
        arrow = Arrow([0, 0.35, 0], [0, -0.4, 0], buff=0, color=MUTED, stroke_width=5)

        def klabel(k):
            return Text(f"Schlüssel k = {k}", font_size=30, color=MUTED).move_to([0, -1.0, 0])

        def trial(k):
            return Text(caesar(cipher, -k), font_size=56, color=WHITE).move_to([0, -2.0, 0])

        self.play(FadeIn(lab), Write(ct), run_time=1.2)
        self.play(GrowArrow(arrow), run_time=0.6)

        kl = klabel(1)
        tr = trial(1)
        self.play(FadeIn(kl), FadeIn(tr), run_time=0.8)
        self.wait(0.8)
        for k in (2, 3):
            self.play(Transform(kl, klabel(k)), Transform(tr, trial(k)), run_time=0.6)
            self.wait(0.8)

        found = Text("Sinnvoller Text gefunden!", font_size=30, color=OK).move_to([0, -3.2, 0])
        self.play(tr.animate.set_color(OK), FadeIn(found, shift=UP * 0.2), run_time=0.8)
        self.wait(1.6)

        only25 = Text(
            "Es gibt nur 25 mögliche Schlüssel – das dauert Sekunden.",
            font_size=28,
            color=WHITE,
        ).move_to([0, -3.2, 0])
        fit(only25)
        self.play(ReplacementTransform(found, only25), run_time=0.8)
        self.wait(2.5)
        self.clear()

    # ---------- 8. Häufigkeitsanalyse ----------
    def frequency_analysis(self):
        head = self.show_title("Schwachstelle 2: Häufigkeitsanalyse")

        # Buchstabenhäufigkeit im Deutschen (in %, gerundet)
        freq = [
            6.5, 1.9, 3.1, 5.1, 17.4, 1.7, 3.0, 4.8, 7.6, 0.3, 1.2, 3.4, 2.5,
            9.8, 2.5, 0.8, 0.02, 7.0, 7.3, 6.2, 4.4, 0.7, 1.9, 0.03, 0.04, 1.1,
        ]
        base = -1.8
        scale = 0.17
        x_of = lambda i: -6.25 + i * 0.5

        axis = Line([-6.6, base, 0], [6.6, base, 0], color=GRAY, stroke_width=2)
        bars = VGroup()
        for i, f in enumerate(freq):
            h = max(f * scale, 0.03)
            bar = Rectangle(
                width=0.36, height=h, fill_color=PLAIN, fill_opacity=0.85, stroke_width=0
            ).move_to([x_of(i), base + h / 2, 0])
            bars.add(bar)
        letters = VGroup(
            *[Text(ch, font_size=20, color=MUTED).move_to([x_of(i), base - 0.3, 0]) for i, ch in enumerate(ALPHA)]
        )

        cap1 = Text("Klartext: So oft kommt jeder Buchstabe im Deutschen vor", font_size=28, color=PLAIN)
        fit(cap1)
        cap1.move_to([0, 2.5, 0])

        self.play(FadeIn(cap1), Create(axis), FadeIn(letters), run_time=1.0)
        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05),
            run_time=2.0,
        )

        # Höchsten Balken (E) hervorheben
        peak_label = Text("E", font_size=30, color=YELLOW, weight=BOLD)
        peak_label.move_to([x_of(4), base + freq[4] * scale + 0.35, 0])
        self.play(bars[4].animate.set_fill(YELLOW, opacity=1), FadeIn(peak_label, shift=DOWN * 0.2))
        self.wait(1.2)

        # Verschlüsseln = alle Balken um 3 Spalten nach rechts schieben (Förderband)
        cap2 = Text("Geheimtext: Das ganze Muster ist um 3 Stellen verschoben", font_size=28, color=CIPHER)
        fit(cap2)
        cap2.move_to([0, 2.5, 0])

        shift_x = RIGHT * SHIFT * 0.5
        incoming = []
        for j, i in enumerate((23, 24, 25)):
            cp = bars[i].copy()
            cp.set_x(x_of(j))          # Zielposition: Spalten A, B, C
            incoming.append(cp)

        self.play(
            *[bars[i].animate.shift(shift_x) for i in range(23)],
            peak_label.animate.shift(shift_x),
            *[FadeOut(bars[i], shift=shift_x) for i in (23, 24, 25)],
            *[FadeIn(cp, shift=shift_x) for cp in incoming],
            ReplacementTransform(cap1, cap2),
            run_time=3.0,
        )
        self.wait(1.0)

        # Auswertung
        msg = Text("Höchster Balken bei H  →  H = E + 3  →  k = 3", font_size=30, color=WHITE)
        fit(msg)
        msg.move_to([0, -3.2, 0])
        self.play(letters[7].animate.set_color(YELLOW).scale(1.4), Write(msg), run_time=1.8)
        self.wait(3.0)
        self.clear()

    # ---------- 9. Zusammenfassung ----------
    def outro(self):
        head = self.show_title("Zusammenfassung")

        items = [
            "Jeder Buchstabe wird um k Stellen verschoben",
            "Mathematisch: (x + k) mod 26",
            "Nur 25 Schlüssel – Brute Force knackt sie sofort",
            "Auch die Häufigkeitsanalyse verrät den Schlüssel",
        ]
        rows = VGroup()
        for s in items:
            dot = Dot(radius=0.07, color=PLAIN)
            tx = Text(s, font_size=32, color=WHITE)
            rows.add(VGroup(dot, tx).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        fit(rows, 12.3)
        rows.move_to([0, 0.4, 0])

        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.9)

        final = Text(
            "Unsicher – aber der Anfang der Kryptografie.",
            font_size=32,
            color=CIPHER,
        ).move_to([0, -2.7, 0])
        fit(final)
        self.play(Write(final), run_time=1.6)
        self.wait(3.0)
        self.clear()
