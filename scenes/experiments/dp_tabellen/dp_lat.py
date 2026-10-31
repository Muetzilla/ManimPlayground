"""Manim Community Edition: DP-Tabelle zur längsten aufsteigenden Teilfolge (LAT).

Rendern:
    manim -pql dp_lat.py LATDPTabelle      # schnelle Vorschau (480p)
    manim -pqh dp_lat.py LATDPTabelle      # Full-HD (1080p)

Beispiel aus den Vorlesungsfolien: A = [1, 8, 9, 5, 6, 7].

Rekursion (i >= 2), mit M(i-1, 0) = -inf:
    M(i, l) = A[i]        falls M(i-1, l-1) < A[i] < M(i-1, l)
              M(i-1, l)   sonst

Die Animation folgt dem Ablauf der Folien 112-122:
Initialisierung -> Zeile für Zeile (kopieren, passendes l suchen, ersetzen)
-> Ergebnis -> Beobachtungen (sortiert, 1 Änderung pro Zeile, binäre Suche,
ein einziges Array, O(n log n)).

Ohne LaTeX lauffähig: alle Texte sind Pango-Text in einer einheitlichen Schrift.
"""
from manim import *
import numpy as np

# ============================ Konfiguration ============================
A = [1, 8, 9, 5, 6, 7]   # Eingabefolge (änderbar, Tabelle wird n x n)
SPEED = 1.0              # >1 = schneller, <1 = langsamer (wirkt auf alle Zeiten)
SHOW_RECAP = True        # Beobachtungen + binäre Suche + O(n log n) am Ende

INF = float("inf")

# Farben
C_BG = "#101827"
C_TEXT = "#F1F5F9"
C_MUTED = "#94A3B8"     # abgeschlossene Zeilen
C_INF = "#64748B"       # unendlich-Einträge (immer gedämpft)
C_BLUE = "#38BDF8"
C_GOLD = "#FBBF24"
C_GREEN = "#4ADE80"
C_RED = "#FB7185"
C_CELL = "#1E293B"
C_GRID = "#475569"
GLOW = 0.28             # Füll-Deckkraft der hervorgehobenen Zelle

# Layout (Manim-Koordinaten; Bildbreite 14.22, Bildhöhe 8)
TABLE_W = 4.8           # Gesamtbreite der Tabelle
TABLE_LEFT = -5.6
TABLE_TOP = 1.65
PX, PW = 0.1, 6.75      # rechtes Panel: linke Kante und Breite
Y_HEAD, Y_CHECK, Y_RES, Y_EXTRA = -0.2, -0.85, -1.5, -2.05


def pick_font():
    """Erste vorhandene serifenlose Schrift, sonst generisches 'sans-serif'."""
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


def fmt(v):
    if v == INF:
        return "∞"
    if v == -INF:
        return "−∞"
    return str(int(v))


def build_dp(A):
    """Berechnet die ganze Tabelle M und pro Zeile die aktualisierte Spalte.

    Rückgabe: M[i-1][l-1] sowie hits[i-1] = (i, l) mit der Spalte l, in die A[i]
    geschrieben wird (None, falls keine Spalte die Bedingung erfüllt).
    """
    n = len(A)
    M = [[INF] * n for _ in range(n)]
    M[0][0] = A[0]
    hits = [(1, 1)]
    for i in range(2, n + 1):
        a = A[i - 1]
        prev = M[i - 2]
        M[i - 1] = prev[:]
        hit = None
        for l in range(1, n + 1):
            lo = -INF if l == 1 else prev[l - 2]
            if lo < a < prev[l - 1]:
                hit = l
                M[i - 1][l - 1] = a
                break
        hits.append((i, hit))
    return M, hits


def bin_steps(row, a):
    """Binäre Suche nach der ersten Spalte l mit row[l] >= a (1-basiert)."""
    lo, hi = 1, len(row)
    steps = []
    while lo < hi:
        mid = (lo + hi) // 2
        go_left = row[mid - 1] >= a
        steps.append((lo, hi, mid, go_left))
        if go_left:
            hi = mid
        else:
            lo = mid + 1
    return steps, lo


class LATDPTabelle(Scene):
    def construct(self):
        self.camera.background_color = C_BG
        n = len(A)
        M, hits = build_dp(A)

        # ------------------------- Geometrie -------------------------
        CW = TABLE_W / n
        CH = min(0.68, 4.1 / n)
        X0 = TABLE_LEFT + CW / 2
        Y0 = TABLE_TOP - CH / 2
        LBL_A = TABLE_LEFT - 0.42      # Spalte "A[i]"
        LBL_I = TABLE_LEFT - 0.95      # Spalte "i"
        val_size = 26 if n <= 7 else 20

        # ------------------------- Hilfsfunktionen -------------------------
        def rt(t):
            return t / SPEED

        def P(*anims, t=0.6):
            self.play(*anims, run_time=rt(t))

        def W(t):
            self.wait(rt(t))

        def T(s, size=24, color=C_TEXT, **kw):
            return Text(s, font=FONT, font_size=size, color=color, **kw)

        def cell_pos(i, l):
            return np.array([X0 + (l - 1) * CW, Y0 - (i - 1) * CH, 0.0])

        def row_center(i):
            return np.array([X0 + (n - 1) * CW / 2, Y0 - (i - 1) * CH, 0.0])

        def place_left(m, y):
            """Linke Kante des Mobjects an die linke Panelkante, Mitte auf Höhe y."""
            if m.width > PW:
                m.scale_to_fit_width(PW)
            return m.move_to(np.array([PX, y, 0.0]), aligned_edge=LEFT)

        def make_value(v, i, l, current=True, accent=False):
            if v == INF:
                color, kw = C_INF, {}
            elif accent:
                color, kw = C_GREEN, {"weight": BOLD}
            else:
                color, kw = (C_TEXT if current else C_MUTED), {}
            return T(fmt(v), val_size, color, **kw).move_to(cell_pos(i, l))

        def mark(ok):
            if ok:
                m = VMobject()
                m.set_points_as_corners([np.array([-0.14, 0.0, 0.0]),
                                         np.array([-0.04, -0.12, 0.0]),
                                         np.array([0.16, 0.14, 0.0])])
                return m.set_stroke(C_GREEN, 5)
            m = VGroup(Line(np.array([-0.12, -0.12, 0.0]), np.array([0.12, 0.12, 0.0])),
                       Line(np.array([-0.12, 0.12, 0.0]), np.array([0.12, -0.12, 0.0])))
            return m.set_stroke(C_RED, 5)

        def make_check_line(l, lo, a, hi, ok1, ok2):
            parts = VGroup(
                T(f"ℓ = {l}:", 22, C_MUTED),
                T(fmt(lo), 26, C_BLUE, weight=BOLD),
                T("<", 26, C_GREEN if ok1 else C_RED, weight=BOLD),
                T(str(a), 26, C_GOLD, weight=BOLD),
                T("<", 26, C_GREEN if ok2 else C_RED, weight=BOLD),
                T(fmt(hi), 26, C_BLUE, weight=BOLD),
            ).arrange(RIGHT, buff=0.22)
            m = mark(ok1 and ok2)
            m.next_to(parts, RIGHT, buff=0.35)
            return place_left(VGroup(parts, m), Y_CHECK)

        def scan_box_for(i, l):
            """Rahmen um M(i-1, l-1) und M(i-1, l) in der Vorgängerzeile."""
            l0 = max(1, l - 1)
            left = cell_pos(i - 1, l0)[0] - CW / 2
            right = cell_pos(i - 1, l)[0] + CW / 2
            box = Rectangle(width=right - left, height=CH, color=C_BLUE, stroke_width=3.5)
            return box.move_to(np.array([(left + right) / 2, cell_pos(i - 1, 1)[1], 0.0]))

        def step_header(i):
            g = VGroup(T(f"i = {i}", 28, C_BLUE, weight=BOLD),
                       T(f"A[{i}] = {A[i - 1]}", 28, C_GOLD, weight=BOLD)).arrange(RIGHT, buff=0.5)
            return place_left(g, Y_HEAD)

        def make_result(s, color=C_GREEN):
            return place_left(T(s, 26, color, weight=BOLD), Y_RES)

        def bullet(lines, y, size=22, color=C_TEXT, mark_char="–", **kw):
            body = VGroup(*[T(s, size, color, **kw) for s in lines]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            dash = T(mark_char, size, color, **kw)
            g = VGroup(dash, body).arrange(RIGHT, buff=0.2, aligned_edge=UP)
            return place_left(g, y)

        # ------------------------- Titel -------------------------
        title = T("Längste aufsteigende Teilfolge", 38, C_TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        subtitle = T("Merke für jede Länge nur die kleinstmögliche Endung", 24, C_MUTED)
        subtitle.next_to(title, DOWN, buff=0.15)
        P(Write(title), FadeIn(subtitle, shift=UP * 0.1), t=1.4)

        caption = T("M(i, ℓ) = kleinstmögliche Endung einer aufsteigenden Teilfolge "
                    "der Länge ℓ in A[1..i]   (∞, falls es keine gibt)", 20, C_MUTED)
        if caption.width > 12.8:
            caption.scale_to_fit_width(12.8)
        caption.to_edge(DOWN, buff=0.45)

        # ------------------------- Tabelle -------------------------
        cells, rect_list = {}, []
        for i in range(1, n + 1):
            for l in range(1, n + 1):
                r = Rectangle(width=CW, height=CH, color=C_GRID, stroke_width=1.2)
                r.set_fill(C_CELL, opacity=1).move_to(cell_pos(i, l))
                cells[i, l] = r
                rect_list.append(r)
        outer = Rectangle(width=n * CW, height=n * CH, color=C_TEXT, stroke_width=2.4)
        outer.move_to(np.array([X0 + (n - 1) * CW / 2, TABLE_TOP - n * CH / 2, 0.0]))

        head_y = TABLE_TOP + 0.3
        col_heads = VGroup(*[T(str(l), 24, C_BLUE).move_to(np.array([cell_pos(1, l)[0], head_y, 0.0]))
                             for l in range(1, n + 1)])
        len_label = T("Länge ℓ", 20, C_BLUE).move_to(np.array([X0 + (n - 1) * CW / 2, head_y + 0.42, 0.0]))
        hdr_i = T("i", 20, C_MUTED).move_to(np.array([LBL_I, head_y, 0.0]))
        hdr_a = T("A[i]", 22, C_GOLD).move_to(np.array([LBL_A, head_y, 0.0]))
        i_labels = {i: T(str(i), 20, C_MUTED).move_to(np.array([LBL_I, cell_pos(i, 1)[1], 0.0]))
                    for i in range(1, n + 1)}
        a_labels = {i: T(str(A[i - 1]), 28, C_GOLD, weight=BOLD).move_to(
            np.array([LBL_A, cell_pos(i, 1)[1], 0.0])) for i in range(1, n + 1)}

        P(LaggedStart(*[Create(r) for r in rect_list], lag_ratio=0.02),
          Create(outer),
          FadeIn(col_heads), FadeIn(len_label), FadeIn(hdr_i), FadeIn(hdr_a),
          FadeIn(VGroup(*i_labels.values())), FadeIn(VGroup(*a_labels.values())),
          FadeIn(caption, shift=UP * 0.1),
          t=1.8)

        # ------------------------- Rekursionsformel (rechts oben) -------------------------
        f_title = place_left(T("Rekursion (für i ≥ 2, mit M(i−1, 0) = −∞):", 19, C_MUTED), 2.35)
        lhs = T("M(i, ℓ) =", 24, C_TEXT, weight=BOLD)
        r1 = T("A[i],   falls  M(i−1, ℓ−1) < A[i] < M(i−1, ℓ)", 24, C_TEXT, weight=BOLD)
        r2 = T("M(i−1, ℓ),   sonst", 24, C_TEXT, weight=BOLD)
        rest = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        formula = VGroup(lhs, rest).arrange(RIGHT, buff=0.25, aligned_edge=UP)
        place_left(formula, 1.75)
        n1 = T("A[i] passt an eine Folge der Länge ℓ−1", 17, C_RED)
        n2 = T("neue Folge verbessert das bisherige Minimum", 17, C_RED)
        notes = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        notes.move_to(np.array([rest.get_left()[0], 0.78, 0.0]), aligned_edge=LEFT)
        divider = Line(np.array([PX, 0.25, 0.0]), np.array([PX + PW, 0.25, 0.0]),
                       stroke_width=1.2, color=C_GRID)
        formula_stuff = VGroup(f_title, formula, notes, divider)
        P(FadeIn(f_title), Write(formula), t=1.6)
        P(FadeIn(notes, shift=UP * 0.1), Create(divider), t=0.8)
        W(0.5)

        # ------------------------- Initialisierung: Zeile 1 -------------------------
        values = {}
        row_box = Rectangle(width=n * CW, height=CH, color=C_TEXT, stroke_width=2.5)
        row_box.move_to(row_center(1))
        header = place_left(VGroup(T("i = 1", 28, C_BLUE, weight=BOLD),
                                   T("Initialisierung", 26, C_TEXT)).arrange(RIGHT, buff=0.5), Y_HEAD)
        P(Create(row_box), FadeIn(header, shift=RIGHT * 0.2), t=0.8)

        infs = []
        for l in range(2, n + 1):
            v = make_value(INF, 1, l)
            values[1, l] = v
            infs.append(v)
        if infs:
            P(LaggedStart(*[FadeIn(v, scale=0.7) for v in infs], lag_ratio=0.2), t=1.0)
        v11 = make_value(A[0], 1, 1, accent=True)
        values[1, 1] = v11
        result = make_result(f"M(1,1) = A[1] = {A[0]}")
        P(TransformFromCopy(a_labels[1], v11),
          cells[1, 1].animate.set_fill(C_GREEN, opacity=GLOW).set_stroke(C_GREEN, width=2.5),
          FadeIn(result, shift=UP * 0.1), t=1.1)
        W(0.8)

        # ------------------------- Zeilen 2..n -------------------------
        scan_box, check = None, None
        for i in range(2, n + 1):
            a = A[i - 1]
            hit = hits[i - 1][1]
            prev_hit = hits[i - 2][1]
            prev_row = M[i - 2]

            # 1. Zeilenwechsel: Rahmen rutscht nach unten, alte Zeile wird gedämpft
            new_header = step_header(i)
            cleanup = [m for m in (scan_box, check, result) if m is not None]
            anims = [row_box.animate.move_to(row_center(i)),
                     FadeTransform(header, new_header)]
            if cleanup:
                anims.append(FadeOut(*cleanup))
            for l in range(1, n + 1):
                if prev_row[l - 1] != INF:
                    anims.append(values[i - 1, l].animate.set_color(C_MUTED))
            if prev_hit is not None:
                anims.append(cells[i - 1, prev_hit].animate.set_fill(C_CELL, opacity=1)
                             .set_stroke(C_GRID, width=1.2))
            P(*anims, t=0.7)
            header = new_header
            scan_box, check, result = None, None, None

            # 2. Vorherige Zeile in die neue kopieren
            new_vals = {l: make_value(prev_row[l - 1], i, l) for l in range(1, n + 1)}
            P(LaggedStart(*[TransformFromCopy(values[i - 1, l], new_vals[l])
                            for l in range(1, n + 1)], lag_ratio=0.12), t=1.0)
            for l in range(1, n + 1):
                values[i, l] = new_vals[l]

            # 3. Passendes l suchen: M(i-1, l-1) < A[i] < M(i-1, l)
            for l in range(1, n + 1):
                lo = -INF if l == 1 else prev_row[l - 2]
                hi = prev_row[l - 1]
                ok1, ok2 = lo < a, a < hi
                box_new = scan_box_for(i, l)
                check_new = make_check_line(l, lo, a, hi, ok1, ok2)
                if scan_box is None:
                    scan_box = box_new
                    P(Create(scan_box), FadeIn(check_new), t=0.45)
                else:
                    P(Transform(scan_box, box_new), FadeTransform(check, check_new), t=0.4)
                check = check_new
                W(0.3)
                if ok1 and ok2:
                    break

            # 4. Ersetzen (oder: nichts zu tun)
            if hit is not None:
                old = values[i, hit]
                new = make_value(a, i, hit, accent=True)
                result = make_result(f"M({i},{hit}) = A[{i}] = {a}")
                P(cells[i, hit].animate.set_fill(C_GREEN, opacity=GLOW).set_stroke(C_GREEN, width=2.5),
                  FadeOut(old, shift=DOWN * 0.15),
                  TransformFromCopy(a_labels[i], new),
                  FadeIn(result, shift=UP * 0.1), t=1.0)
                values[i, hit] = new
            else:
                result = make_result(f"kein ℓ passt ({a} kommt schon vor) → Zeile bleibt gleich", C_MUTED)
                P(FadeIn(result, shift=UP * 0.1), t=0.6)
            W(0.6)

        # ------------------------- Ergebnis -------------------------
        k = sum(1 for v in M[n - 1] if v != INF)
        ends = " ".join(fmt(v) for v in M[n - 1][:k])
        last_hit = hits[n - 1][1]
        cleanup = [m for m in (scan_box, check, result, header) if m is not None]
        fin_head = place_left(T("Ergebnis", 30, C_GREEN, weight=BOLD), Y_HEAD)
        fin1 = place_left(T(f"{k} endliche Einträge in der letzten Zeile", 24), Y_CHECK)
        fin2 = place_left(T(f"→  längste aufsteigende Teilfolge hat Länge {k}", 24, C_GREEN, weight=BOLD), Y_RES)
        fin3 = place_left(T(f"Endungen: {ends}", 22, C_MUTED), Y_EXTRA)
        res_box = SurroundingRectangle(VGroup(*[cells[n, l] for l in range(1, k + 1)]),
                                       color=C_GREEN, buff=0.03, stroke_width=4.5)
        anims = [FadeOut(*cleanup), FadeOut(row_box), Create(res_box),
                 FadeIn(fin_head), FadeIn(fin1, shift=UP * 0.1)]
        if last_hit is not None:
            anims.append(cells[n, last_hit].animate.set_fill(C_CELL, opacity=1).set_stroke(C_GRID, width=1.2))
        P(*anims, t=1.0)
        P(FadeIn(fin2, shift=UP * 0.1), FadeIn(fin3, shift=UP * 0.1), t=0.9)
        W(2.0)

        if not SHOW_RECAP:
            W(1.0)
            return

        # ------------------------- Beobachtungen -------------------------
        # Tabelle für den Rückblick: endliche Werte hell, Rest gedämpft
        finite_vals = [values[i, l] for i in range(1, n + 1) for l in range(1, n + 1) if M[i - 1][l - 1] != INF]
        recap_title = place_left(T("Beobachtung:", 30, C_TEXT, weight=BOLD), 2.4)
        P(FadeOut(formula_stuff), FadeOut(fin_head, fin1, fin2, fin3), FadeOut(res_box),
          VGroup(*finite_vals).animate.set_color(C_TEXT),
          FadeIn(recap_title), t=1.0)

        # (1) Zeilen sind sortiert
        b1 = bullet(["Zeilen sind sortiert."], 1.85)
        P(FadeIn(b1, shift=RIGHT * 0.2), t=0.6)
        boxes = []
        for r in range(1, n + 1):
            cnt = sum(1 for v in M[r - 1] if v != INF)
            boxes.append(SurroundingRectangle(VGroup(*[cells[r, l] for l in range(1, cnt + 1)]),
                                              color=C_BLUE, buff=0.0, stroke_width=3))
        P(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25), t=2.0)
        W(0.6)
        P(FadeOut(*boxes), t=0.5)

        # (2) pro Zeile nur ein Eintrag ändert sich
        b2 = bullet(["Wir ändern pro Zeile nur einen Eintrag."], 1.35)
        P(FadeIn(b2, shift=RIGHT * 0.2), t=0.6)
        upd = [(i, l) for (i, l) in hits if l is not None]
        P(LaggedStart(*[AnimationGroup(
            cells[c].animate.set_fill(C_GREEN, opacity=GLOW).set_stroke(C_GREEN, width=2.5),
            values[c].animate.set_color(C_GREEN)) for c in upd], lag_ratio=0.3), t=2.0)
        W(0.6)

        # (3) binäre Suche
        b3 = bullet(["Diesen können wir mit binärer Suche", "in Zeit O(log n) finden."], 0.7)
        P(FadeIn(b3, shift=RIGHT * 0.2), t=0.6)
        if n >= 2:
            row = n - 1
            prow, a_last = M[n - 2], A[n - 1]
            steps, found = bin_steps(prow, a_last)

            def rng_box(lo, hi):
                left = cell_pos(row, lo)[0] - CW / 2
                right = cell_pos(row, hi)[0] + CW / 2
                r = Rectangle(width=right - left, height=CH, color=C_BLUE, stroke_width=3.5)
                r.set_fill(C_BLUE, opacity=0.14)
                return r.move_to(np.array([(left + right) / 2, cell_pos(row, 1)[1], 0.0]))

            def mid_box(m, color=C_GOLD):
                return Rectangle(width=CW - 0.08, height=CH - 0.08, color=color,
                                 stroke_width=4.5).move_to(cell_pos(row, m))

            def status(s, color=C_BLUE):
                return place_left(T(s, 22, color), -1.6)

            bs_box = rng_box(1, n)
            st = status(f"Suche erste Endung ≥ {a_last} in Zeile {row}")
            P(Create(bs_box), FadeIn(st), t=0.8)
            m_box = None
            for (lo, hi, mid, go_left) in steps:
                nb, nm = rng_box(lo, hi), mid_box(mid)
                ns = status(f"mid = {mid}:  M({row},{mid}) = {fmt(prow[mid - 1])} "
                            f"{'≥' if go_left else '<'} {a_last}  →  {'links' if go_left else 'rechts'}")
                if m_box is None:
                    m_box = nm
                    P(Transform(bs_box, nb), Create(m_box), FadeTransform(st, ns), t=0.8)
                else:
                    P(Transform(bs_box, nb), Transform(m_box, nm), FadeTransform(st, ns), t=0.8)
                st = ns
                W(0.7)
            fs = status(f"gefunden: ℓ = {found}   ({len(steps)} Vergleiche statt bis zu {n})", C_GREEN)
            fb = rng_box(found, found)
            if m_box is not None:
                P(Transform(bs_box, fb), Transform(m_box, mid_box(found, C_GREEN)),
                  FadeTransform(st, fs), t=0.8)
            else:
                P(Transform(bs_box, fb), FadeTransform(st, fs), t=0.8)
            W(1.0)
            gone = [m for m in (bs_box, m_box, fs) if m is not None]
            P(FadeOut(*gone), t=0.5)

        # (4) ein einziges Array wiederverwenden
        b4 = bullet(["Wenn wir dasselbe Array für jede Zeile",
                     "wiederverwenden, dauert das Update",
                     "pro Zeile nur O(log n)."], -0.3)
        P(FadeIn(b4, shift=RIGHT * 0.2), t=0.6)
        mw = 0.7
        mini = VGroup(*[Rectangle(width=mw, height=0.6, color=C_GRID, stroke_width=1.6)
                        .set_fill(C_CELL, opacity=1) for _ in range(n)]).arrange(RIGHT, buff=0)
        mini.move_to(np.array([PX + n * mw / 2, -2.1, 0.0]))
        mini_label = place_left(T("ein einziges Array – es wird nur verändert", 19, C_MUTED), -1.62)
        arr_vals = [T("∞", 26, C_INF).move_to(mini[k_].get_center()) for k_ in range(n)]
        rb = Rectangle(width=n * CW, height=CH, color=C_TEXT, stroke_width=2.5).move_to(row_center(1))
        P(FadeIn(mini), FadeIn(mini_label), FadeIn(VGroup(*arr_vals)), Create(rb), t=0.9)
        for i in range(1, n + 1):
            hit = hits[i - 1][1]
            anims = []
            if i > 1:
                anims.append(rb.animate.move_to(row_center(i)))
            if hit is not None:
                new = T(str(A[i - 1]), 26, C_TEXT).move_to(mini[hit - 1].get_center())
                anims.append(ReplacementTransform(arr_vals[hit - 1], new))
                arr_vals[hit - 1] = new
            if anims:
                P(*anims, t=0.6)
            if hit is not None:
                P(Indicate(arr_vals[hit - 1], color=C_GREEN, scale_factor=1.4), t=0.5)
            W(0.15)
        P(FadeOut(rb), t=0.4)

        # (5) Gesamtlaufzeit
        b5 = bullet(["insgesamt Laufzeit O(n log n)"], -1.05, size=26, color=C_GREEN,
                    mark_char="→", weight=BOLD)
        P(FadeIn(b5, shift=RIGHT * 0.2), t=0.8)
        W(3.0)