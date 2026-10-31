"""Manim Community Edition: Lemma 1.26 – m linear unabhängige Vektoren spannen R^m auf.

Rendern:
    manim -pql lemma_1_26.py Lemma126      # schnelle Vorschau (480p)
    manim -pqh lemma_1_26.py Lemma126      # Full-HD (1080p)

Idee des Beweises (Austauschverfahren), hier an einem konkreten Beispiel in R^3:
  Start:  e1, e2, e3                       Span = R^3
  Schritt k: v_k direkt hinter v_(k-1) einfügen -> m+1 Vektoren in R^m, also linear
             abhängig -> einer der Vektoren ist Linearkombination der vorherigen.
             Das kann kein v sein (v1..vk sind unabhängig), also ist es ein e_i.
             e_i entfernen -> Span bleibt R^m.
  Ende:   v1, v2, v3                       Span = R^3

Der entfernte Vektor wird wirklich berechnet (exakte Bruchrechnung): die Animation zeigt
die Linearkombination, z. B. e2 = ½·v1 − ½·e1. Die Vektoren V sind frei wählbar,
müssen aber linear unabhängig sein (wird geprüft).

Gleicher Stil wie dp_lat.py / dp_arr.py (Farben, Schrift, Tempo). Ohne LaTeX lauffähig.
"""
from fractions import Fraction

from manim import *
import numpy as np

# ============================ Konfiguration ============================
V = [(1, 2, 0), (0, 1, 1), (1, 0, 1)]   # v1..vm in R^m (linear unabhängig!)
SPEED = 1.0                              # >1 = schneller, <1 = langsamer

# Farben (identisch zu den anderen Animationen)
C_BG = "#101827"
C_TEXT = "#F1F5F9"
C_MUTED = "#94A3B8"
C_BLUE = "#38BDF8"      # Einheitsvektoren e_i
C_GOLD = "#FBBF24"      # Vektoren v_i
C_GREEN = "#4ADE80"
C_RED = "#FB7185"
C_CELL = "#1E293B"
C_GRID = "#475569"

# Layout
Y_ROW = 0.45                       # Mitte der Vektor-Karten
Y_STEP, Y_GIVEN = 2.35, 2.0        # Schrittzähler / "Gegeben"-Zeile (ganz oben)
Y_STAT, Y_SPAN, Y_NOTE = -1.75, -2.6, -3.4
CARD_W, CARD_H = 1.15, 1.9


def pick_font():
    prefs = ["Inter", "Helvetica Neue", "Helvetica", "Arial", "Segoe UI",
             "DejaVu Sans", "Liberation Sans", "Noto Sans"]
    try:
        import manimpango
        available = set(manimpango.list_fonts())
        for f in prefs:
            if f in available:
                return f
    except Exception:
        pass
    return "sans-serif"


FONT = pick_font()


def sup(m):
    return "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] for c in str(m))


def solve(cols, x):
    """Löst sum_j c_j * cols[j] = x exakt (Fractions); None, falls nicht darstellbar."""
    rows, k = len(x), len(cols)
    if k == 0:
        return [] if all(v == 0 for v in x) else None
    Mx = [[Fraction(cols[j][r]) for j in range(k)] + [Fraction(x[r])] for r in range(rows)]
    piv, row = [], 0
    for c in range(k):
        p = next((r for r in range(row, rows) if Mx[r][c] != 0), None)
        if p is None:
            continue
        Mx[row], Mx[p] = Mx[p], Mx[row]
        pv = Mx[row][c]
        Mx[row] = [v / pv for v in Mx[row]]
        for r in range(rows):
            if r != row and Mx[r][c] != 0:
                f = Mx[r][c]
                Mx[r] = [a - f * b for a, b in zip(Mx[r], Mx[row])]
        piv.append(c)
        row += 1
    if any(Mx[r][k] != 0 for r in range(row, rows)):
        return None
    coeffs = [Fraction(0)] * k
    for r, c in enumerate(piv):
        coeffs[c] = Mx[r][k]
    return coeffs


def frac_txt(c):
    c = abs(c)
    if c.denominator == 1:
        return "" if c == 1 else str(c.numerator)
    if c == Fraction(1, 2):
        return "½"
    return f"{c.numerator}/{c.denominator}"


def lin_comb_txt(names, coeffs):
    out = ""
    for nm, c in zip(names, coeffs):
        if c == 0:
            continue
        mag = frac_txt(c)
        term = (mag + "·" if mag else "") + nm
        if not out:
            out = ("−" if c < 0 else "") + term
        else:
            out += f" {'−' if c < 0 else '+'} {term}"
    return out or "0"


class Lemma126(Scene):
    def construct(self):
        self.camera.background_color = C_BG
        m = len(V)
        assert all(len(v) == m for v in V), "Jeder Vektor braucht genau m Einträge."
        assert all(solve(V[:j], V[j]) is None for j in range(m)), \
            "Die Vektoren V müssen linear unabhängig sein."

        vec = {f"v{j + 1}": tuple(V[j]) for j in range(m)}
        for j in range(m):
            vec[f"e{j + 1}"] = tuple(1 if r == j else 0 for r in range(m))

        SP = min(2.0, 11.5 / (m + 1))          # Abstand der Karten

        # ------------------------- Hilfsfunktionen -------------------------
        def rt(t):
            return t / SPEED

        def P(*anims, t=0.6):
            self.play(*anims, run_time=rt(t))

        def W(t):
            self.wait(rt(t))

        def T(s, size=24, color=C_TEXT, **kw):
            return Text(s, font=FONT, font_size=size, color=color, **kw)

        def at(m_, y, x=0.0):
            return m_.move_to(np.array([x, y, 0.0]))

        def fit(m_, w=12.8):
            if m_.width > w:
                m_.scale_to_fit_width(w)
            return m_

        def swap(old, new, **kw):
            return FadeTransform(old, new) if old is not None else FadeIn(new)

        def name_color(nm):
            return C_GOLD if nm.startswith("v") else C_BLUE

        def make_card(nm):
            col = name_color(nm)
            rect = Rectangle(width=CARD_W, height=CARD_H, color=col, stroke_width=3)
            rect.set_fill(C_CELL, opacity=1)
            ents = VGroup(*[T(str(x), 30, col if x != 0 or nm.startswith("v") else C_MUTED,
                              weight=BOLD if nm.startswith("v") else "NORMAL")
                            for x in vec[nm]]).arrange(DOWN, buff=0.28)
            ents.move_to(rect.get_center())
            label = T(nm, 32, col, weight=BOLD).next_to(rect, UP, buff=0.15)
            return VGroup(rect, ents, label)

        def rect_of(nm):
            return cards[nm][0]

        def tx(idx, count):
            return (idx - (count - 1) / 2) * SP

        def place(nm, x):
            card = cards[nm]
            card.shift(np.array([x, Y_ROW, 0.0]) - card[0].get_center())

        def dx_to(nm, x):
            return np.array([x - rect_of(nm).get_center()[0], 0.0, 0.0])

        def mark(ok):
            if ok:
                mk = VMobject()
                mk.set_points_as_corners([np.array([-0.16, 0.0, 0.0]),
                                          np.array([-0.05, -0.14, 0.0]),
                                          np.array([0.18, 0.16, 0.0])])
                return mk.set_stroke(C_GREEN, 6)
            mk = VGroup(Line(np.array([-0.14, -0.14, 0.0]), np.array([0.14, 0.14, 0.0])),
                        Line(np.array([-0.14, 0.14, 0.0]), np.array([0.14, -0.14, 0.0])))
            return mk.set_stroke(C_RED, 6)

        def span_line(names, final=False):
            c = C_GREEN if final else C_TEXT
            parts = [T("Span(", 32, c)]
            for j, nm in enumerate(names):
                if j:
                    parts.append(T(",", 32, C_MUTED))
                parts.append(T(nm, 32, name_color(nm), weight=BOLD))
            parts.append(T(f")  =  R{sup(m)}", 32, c, weight=BOLD if final else "NORMAL"))
            return at(VGroup(*parts).arrange(RIGHT, buff=0.12), Y_SPAN)

        def status_text(s, color=C_TEXT, size=28, weight="NORMAL"):
            return at(fit(T(s, size, color, weight=weight)), Y_STAT)

        def note_text(s, color=C_MUTED):
            return at(fit(T(s, 22, color)), Y_NOTE)

        def step_text(k):
            return at(T(f"Austauschschritt {k} von {m}", 24, C_BLUE), Y_STEP)

        # ------------------------- Titel -------------------------
        title = T(f"Lemma 1.26: Span von {m} unabhängigen Vektoren", 38, C_TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        fit(title, 13.2)
        subtitle = T(f"Beweisidee: Einheitsvektoren Schritt für Schritt durch die v_i ersetzen",
                     24, C_MUTED)
        subtitle.next_to(title, DOWN, buff=0.15)
        fit(subtitle, 13.2)
        P(Write(title), FadeIn(subtitle, shift=UP * 0.1), t=1.6)

        given_txt = ",   ".join(f"v{j + 1} = ({', '.join(str(x) for x in V[j])})" for j in range(m))
        given = at(fit(T(f"Gegeben (linear unabhängig):   {given_txt}", 22, C_MUTED)), Y_GIVEN)
        P(FadeIn(given, shift=UP * 0.1), t=0.8)

        # ------------------------- Start: e1..em -------------------------
        seq = [f"e{j + 1}" for j in range(m)]
        cards = {}
        for idx, nm in enumerate(seq):
            cards[nm] = make_card(nm)
            place(nm, tx(idx, m))
        P(LaggedStart(*[FadeIn(cards[nm], shift=UP * 0.2) for nm in seq], lag_ratio=0.25), t=1.2)

        span_mob = span_line(seq)
        u_sum = " + ".join(f"u{j + 1}·e{j + 1}" for j in range(m))
        note = note_text(f"jedes u in R{sup(m)} ist  u = {u_sum}  →  der Span ist der ganze Raum")
        P(FadeIn(span_mob, shift=UP * 0.1), FadeIn(note, shift=UP * 0.1), t=1.0)
        W(1.8)

        status, step_mob, hl = None, None, None

        # ------------------------- Austauschschritte -------------------------
        for k in range(1, m + 1):
            vname = f"v{k}"

            # 1. v_k direkt hinter v_(k-1) einfügen
            seq.insert(k - 1, vname)
            count = len(seq)
            cards[vname] = make_card(vname)
            place(vname, tx(k - 1, count))
            new_step = step_text(k)
            new_status = status_text(
                f"füge {vname} " + ("vor die Einheitsvektoren ein" if k == 1
                                    else f"direkt nach v{k - 1} ein"), C_GOLD, 28, BOLD)
            new_span = span_line(seq)
            new_note = note_text(f"{count} Vektoren in R{sup(m)}  →  linear abhängig", C_TEXT)
            moves = [cards[nm].animate.shift(dx_to(nm, tx(idx, count)))
                     for idx, nm in enumerate(seq) if nm != vname]
            P(FadeIn(cards[vname], shift=DOWN * 0.8), *moves,
              swap(step_mob, new_step), swap(status, new_status),
              FadeTransform(span_mob, new_span), FadeTransform(note, new_note), t=1.1)
            step_mob, status, span_mob, note = new_step, new_status, new_span, new_note
            W(0.5)

            # 2. von links nach rechts prüfen: ist der Vektor Linearkombination der vorherigen?
            marks = []
            dep, eq = None, None
            for idx, nm in enumerate(seq):
                coeffs = solve([vec[p] for p in seq[:idx]], vec[nm])
                center = rect_of(nm).get_center()
                box = Rectangle(width=CARD_W + 0.28, height=CARD_H + 0.28, color=C_BLUE,
                                stroke_width=4.5).move_to(center)
                if coeffs is None:
                    mk = mark(True).move_to(center + DOWN * 1.35)
                    marks.append(mk)
                    msg = (f"{nm}: keine Linearkombination der vorherigen" if idx
                           else f"{nm}: erster Vektor, ungleich 0")
                    ns = status_text(msg, C_GREEN, 26)
                    if hl is None:
                        hl = box
                        P(Create(hl), FadeIn(mk), swap(status, ns), t=0.6)
                    else:
                        P(Transform(hl, box), FadeIn(mk), swap(status, ns), t=0.6)
                    status = ns
                    W(0.25)
                else:
                    dep = nm
                    eq = f"{nm} = {lin_comb_txt(seq[:idx], coeffs)}"
                    mk = mark(False).move_to(center + DOWN * 1.35)
                    marks.append(mk)
                    ns = status_text(eq, C_RED, 30, BOLD)
                    red = Rectangle(width=CARD_W + 0.28, height=CARD_H + 0.28, color=C_RED,
                                    stroke_width=5).move_to(center)
                    if hl is None:
                        hl = red
                        P(Create(hl), FadeIn(mk), swap(status, ns), t=0.8)
                    else:
                        P(Transform(hl, red), FadeIn(mk), swap(status, ns), t=0.8)
                    status = ns
                    break
            assert dep is not None and dep.startswith("e"), "Lemma-Logik verletzt"
            new_note = note_text(f"{dep} ist Linearkombination der vorherigen Vektoren "
                                 f"(kein v kann das sein, v1..v{k} sind unabhängig)", C_TEXT)
            P(FadeTransform(note, new_note), t=0.6)
            note = new_note
            W(1.4)

            # 3. e_i entfernen: Span bleibt R^m
            seq.remove(dep)
            count = len(seq)
            new_status = status_text(f"{dep} entfernen ändert den Span nicht", C_GREEN, 28, BOLD)
            new_span = span_line(seq)
            new_note = note_text(f"{count} Vektoren,  Span bleibt R{sup(m)}", C_TEXT)
            moves = [cards[nm].animate.shift(dx_to(nm, tx(idx, count)))
                     for idx, nm in enumerate(seq)]
            P(FadeOut(cards[dep], shift=DOWN * 0.8), FadeOut(hl), FadeOut(*marks), *moves,
              FadeTransform(status, new_status), FadeTransform(span_mob, new_span),
              FadeTransform(note, new_note), t=1.2)
            status, span_mob, note = new_status, new_span, new_note
            hl = None
            del cards[dep]
            W(0.8)

        # ------------------------- Ergebnis -------------------------
        final_span = span_line(seq, final=True)
        end_box = Square(side_length=0.3, color=C_GREEN, stroke_width=3)
        end_box.next_to(final_span, RIGHT, buff=0.4)
        final_status = status_text("alle Einheitsvektoren sind durch v1, …, v"
                                   f"{m} ersetzt – der Span ist immer R{sup(m)} geblieben",
                                   C_GREEN, 28, BOLD)
        final_note = note_text(f"{m} linear unabhängige Vektoren in R{sup(m)} spannen R{sup(m)} auf")
        P(FadeTransform(span_mob, final_span), Create(end_box),
          FadeTransform(status, final_status), FadeTransform(note, final_note),
          *[cards[nm][0].animate.set_stroke(C_GREEN, width=4) for nm in seq], t=1.4)
        W(3.5)
