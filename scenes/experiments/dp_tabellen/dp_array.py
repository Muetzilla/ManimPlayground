"""Manim Community Edition: LAT, Versuch 5 – ein einzelnes Array, das laufend aktualisiert wird.

Rendern:
    manim -pql dp_arr.py LATArray      # schnelle Vorschau (480p)
    manim -pqh dp_arr.py LATArray      # Full-HD (1080p)

Beispiel aus den Vorlesungsfolien 123-135:
    A = [2, 13, 17, 9, 11, 4, 78, 28, 15, 25, 99]

Ablauf:
  Start (M(*,1) = A[1], Rest unendlich) -> für jedes A[i] die erste Spalte ℓ mit
  M(*,ℓ) >= A[i] per binärer Suche finden und dort A[i] eintragen (alter Wert wird
  durchgestrichen, neuer Wert darunter geschrieben) -> Speicher O(n), Laufzeit
  O(n log n) -> Rückverfolgen über gespeicherte Vorgänger.

Gleicher Stil wie dp_lat.py (Farben, Schrift, Tempo). Ohne LaTeX lauffähig.
"""
from bisect import bisect_left

from manim import *
import numpy as np

# ============================ Konfiguration ============================
A = [2, 13, 17, 9, 11, 4, 78, 28, 15, 25, 99]   # Eingabefolge (änderbar)
SPEED = 1.0           # >1 = schneller, <1 = langsamer
SHOW_SEARCH = True    # binäre Suche pro Element zeigen (False = kürzeres Video)

INF = float("inf")

# Farben (identisch zu dp_lat.py)
C_BG = "#101827"
C_TEXT = "#F1F5F9"
C_MUTED = "#94A3B8"
C_INF = "#64748B"
C_BLUE = "#38BDF8"
C_GOLD = "#FBBF24"
C_GREEN = "#4ADE80"
C_RED = "#FB7185"
C_CELL = "#1E293B"
C_GRID = "#475569"
GLOW = 0.28

# Layout (Bildbreite 14.22, Bildhöhe 8)
BX = -6.4                                   # linke Kante der Textzeilen unten
Y_A, Y_IDX = 1.65, 1.05                     # Array A und seine Indizes
Y_L, Y_LINE, Y_M0, ROW_H = 0.4, 0.08, -0.32, 0.5
Y_S1, Y_S2, Y_S3 = -2.75, -3.25, -3.65      # Statuszeilen


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


def fmt(v):
    if v == INF:
        return "∞"
    return str(int(v))


def bin_steps(row, a):
    """Binäre Suche nach der ersten Spalte l (1-basiert) mit row[l] >= a."""
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


def simulate(A):
    """Spielt den Algorithmus durch.

    Rückgabe: events (pro Element Suchschritte, Spalte l, alter Wert, geändert?),
    K (Anzahl Spalten = Länge der LAT + 1, wie in den Folien), chain (Indizes der
    Rückverfolgung, vom letzten Element zum ersten).
    """
    tails = []
    for a in A:
        p = bisect_left(tails, a)
        if p == len(tails):
            tails.append(a)
        else:
            tails[p] = a
    K = len(tails) + 1

    M = [INF] * K
    idx = [None] * K
    pred_of = {}
    events = []
    for i, a in enumerate(A, 1):
        steps, l = bin_steps(M, a)
        old = M[l - 1]
        changed = old != a
        if changed:
            pred_of[i] = idx[l - 2] if l > 1 else None
            M[l - 1] = a
            idx[l - 1] = i
        events.append(dict(i=i, a=a, steps=steps, l=l, old=old, changed=changed))

    final_len = sum(1 for v in M if v != INF)
    chain = []
    j = idx[final_len - 1] if final_len else None
    while j is not None:
        chain.append(j)
        j = pred_of.get(j)
    return events, K, chain


class LATArray(Scene):
    def construct(self):
        self.camera.background_color = C_BG
        n = len(A)
        events, K, chain = simulate(A)

        # ------------------------- Geometrie -------------------------
        CWA = min(0.98, 11.0 / n)                    # Zellbreite von A
        AX0 = -5.9 + CWA / 2
        MS = min(1.15, 8.4 / max(K - 1, 1))          # Spaltenabstand von M
        XM0 = -5.0

        def xa(j):
            return AX0 + (j - 1) * CWA

        def xm(l):
            return XM0 + (l - 1) * MS

        def mpos(l, d):
            return np.array([xm(l), Y_M0 - d * ROW_H, 0.0])

        # ------------------------- Hilfsfunktionen -------------------------
        def rt(t):
            return t / SPEED

        def P(*anims, t=0.6):
            self.play(*anims, run_time=rt(t))

        def W(t):
            self.wait(rt(t))

        def T(s, size=24, color=C_TEXT, **kw):
            return Text(s, font=FONT, font_size=size, color=color, **kw)

        def place_bl(m, y):
            """Linke Kante an BX, vertikale Mitte auf y; zu breite Texte werden skaliert."""
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
            return m.move_to(np.array([BX, y, 0.0]), aligned_edge=LEFT)

        def header_group(i, a):
            g = VGroup(T(f"i = {i}", 28, C_BLUE, weight=BOLD),
                       T(f"A[{i}] = {a}", 28, C_GOLD, weight=BOLD)).arrange(RIGHT, buff=0.5)
            return place_bl(g, Y_S1)

        def band_box(lo, hi, extra=0):
            """Band über den Spalten lo..hi (Suchbereich).

            Die Höhe reicht nur bis zur tiefsten aktuell belegten Zeile dieser Spalten
            (extra = 1: eine Zeile mehr, für den gerade neu eingetragenen Wert).
            """
            left, right = xm(lo) - MS / 2, xm(hi) + MS / 2
            d = max(depth[c] for c in range(lo, hi + 1)) + extra
            top = Y_L + 0.2
            bottom = Y_M0 - d * ROW_H - 0.3
            r = Rectangle(width=right - left, height=top - bottom, color=C_BLUE, stroke_width=3.5)
            r.set_fill(C_BLUE, opacity=0.12)
            return r.move_to(np.array([(left + right) / 2, (top + bottom) / 2, 0.0]))

        def mid_box(l, color=C_GOLD):
            """Rahmen um den aktuellen Wert von Spalte l."""
            return Rectangle(width=min(MS - 0.15, 0.95), height=0.46, color=color,
                             stroke_width=4.5).move_to(cur[l].get_center())

        # ------------------------- Titel -------------------------
        title = T("Längste aufsteigende Teilfolge", 38, C_TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        subtitle = T("Ein einzelnes Array, das laufend aktualisiert wird", 24, C_MUTED)
        subtitle.next_to(title, DOWN, buff=0.15)
        P(Write(title), FadeIn(subtitle, shift=UP * 0.1), t=1.4)

        # ------------------------- Array A -------------------------
        a_cells, a_texts, a_idx, col_groups = {}, {}, {}, []
        for j in range(1, n + 1):
            r = Rectangle(width=CWA, height=0.75, color=C_GRID, stroke_width=1.4)
            r.set_fill(C_CELL, opacity=1).move_to(np.array([xa(j), Y_A, 0.0]))
            t = T(str(A[j - 1]), 26, C_TEXT, weight=BOLD).move_to(np.array([xa(j), Y_A, 0.0]))
            ix = T(str(j), 16, C_MUTED).move_to(np.array([xa(j), Y_IDX, 0.0]))
            a_cells[j], a_texts[j], a_idx[j] = r, t, ix
            col_groups.append(VGroup(r, t, ix))
        a_outer = Rectangle(width=n * CWA, height=0.75, color=C_TEXT, stroke_width=2.4)
        a_outer.move_to(np.array([AX0 + (n - 1) * CWA / 2, Y_A, 0.0]))
        a_label = T("A:", 24, C_GOLD, weight=BOLD).move_to(np.array([-6.5, Y_A, 0.0]))
        P(LaggedStart(*[FadeIn(g, shift=DOWN * 0.15) for g in col_groups], lag_ratio=0.1),
          Create(a_outer), FadeIn(a_label), t=1.8)

        # ------------------------- Array M (Spalten ℓ = 1..K) -------------------------
        l_label = T("ℓ =", 20, C_BLUE).move_to(np.array([-5.75, Y_L, 0.0]))
        l_heads = VGroup(*[T(str(l), 24, C_BLUE).move_to(np.array([xm(l), Y_L, 0.0]))
                           for l in range(1, K + 1)])
        m_line = Line(np.array([-5.5, Y_LINE, 0.0]), np.array([xm(K) + MS / 2, Y_LINE, 0.0]),
                      stroke_width=1.6, color=C_MUTED)
        m_label = T("M(*, ℓ):", 22, C_TEXT, weight=BOLD).move_to(np.array([-6.2, Y_M0, 0.0]))
        cur = {l: T("∞", 26, C_INF).move_to(mpos(l, 0)) for l in range(1, K + 1)}
        depth = {l: 0 for l in range(1, K + 1)}
        M_now = [INF] * K
        P(FadeIn(l_label), FadeIn(l_heads), Create(m_line), FadeIn(m_label),
          LaggedStart(*[FadeIn(cur[l], scale=0.7) for l in range(1, K + 1)], lag_ratio=0.12),
          t=1.4)

        # ------------------------- Start: M(*,1) = A[1] -------------------------
        hl = Rectangle(width=CWA, height=0.75, color=C_GOLD, stroke_width=4)
        hl.set_fill(C_GOLD, opacity=GLOW).move_to(np.array([xa(1), Y_A, 0.0]))
        s1 = place_bl(VGroup(T("Start", 28, C_BLUE, weight=BOLD),
                             T(f"M(*, 1) = A[1] = {A[0]},   alle anderen Einträge ∞", 24, C_TEXT)
                             ).arrange(RIGHT, buff=0.5), Y_S1)
        P(FadeIn(hl), FadeIn(s1, shift=UP * 0.1), t=0.8)
        old = cur[1]
        newv = T(str(A[0]), 26, C_GREEN, weight=BOLD).move_to(mpos(1, 0))
        P(FadeOut(old), TransformFromCopy(a_texts[1], newv), t=1.0)
        cur[1] = newv
        last_new = newv
        M_now[0] = A[0]
        W(0.8)

        # ------------------------- Elemente 2..n -------------------------
        s2, band, mbox = None, None, None
        for ev in events[1:]:
            i, a, l = ev["i"], ev["a"], ev["l"]

            # 1. Zeiger auf A[i], Aufräumen
            new_s1 = header_group(i, a)
            anims = [hl.animate.move_to(np.array([xa(i), Y_A, 0.0])),
                     FadeTransform(s1, new_s1),
                     last_new.animate.set_color(C_TEXT)]
            left = [m for m in (band, mbox, s2) if m is not None]
            if left:
                anims.append(FadeOut(*left))
            P(*anims, t=0.6)
            s1 = new_s1
            band, mbox, s2 = None, None, None

            # 2. Binäre Suche: erste Spalte ℓ mit M(*,ℓ) >= A[i]
            if SHOW_SEARCH and ev["steps"]:
                band = band_box(1, K)
                s2 = place_bl(T(f"binäre Suche: erste Endung ≥ {a}", 22, C_BLUE), Y_S2)
                P(Create(band), FadeIn(s2), t=0.5)
                for (lo, hi, mid, go_left) in ev["steps"]:
                    nb, nm = band_box(lo, hi), mid_box(mid)
                    sign = "≥" if go_left else "<"
                    where = "links" if go_left else "rechts"
                    ns = place_bl(T(f"mid = {mid}:  M[{mid}] = {fmt(M_now[mid - 1])} {sign} {a}"
                                    f"  →  {where}", 22, C_TEXT), Y_S2)
                    if mbox is None:
                        mbox = nm
                        P(Transform(band, nb), Create(mbox), FadeTransform(s2, ns), t=0.5)
                    else:
                        P(Transform(band, nb), Transform(mbox, nm), FadeTransform(s2, ns), t=0.5)
                    s2 = ns
                    W(0.25)

            # 3. Ergebnis der Suche markieren und eintragen
            fm = mid_box(l, C_GREEN)
            upd = []
            if band is not None:
                upd += [Transform(band, band_box(l, l, extra=1 if ev["changed"] else 0)),
                        Transform(mbox, fm)]
            else:
                mbox = fm
                upd.append(Create(mbox))

            if ev["changed"]:
                old_val = M_now[l - 1]
                old = cur[l]
                newv = T(str(a), 26, C_GREEN, weight=BOLD).move_to(mpos(l, depth[l] + 1))
                strike = Line(old.get_left() + LEFT * 0.06, old.get_right() + RIGHT * 0.06,
                              color=C_MUTED, stroke_width=2.5)
                s2new = place_bl(T(f"ℓ = {l}:   {fmt(old_val)} wird durch {a} ersetzt", 24,
                                   C_GREEN, weight=BOLD), Y_S2)
                if old_val != INF:
                    upd.append(old.animate.set_color(C_MUTED))
                upd += [Create(strike), TransformFromCopy(a_texts[i], newv)]
            else:
                s2new = place_bl(T(f"ℓ = {l}:   {a} steht schon im Array → keine Änderung", 24,
                                   C_MUTED), Y_S2)
            upd.append(FadeTransform(s2, s2new) if s2 is not None else FadeIn(s2new))
            P(*upd, t=1.0)
            s2 = s2new
            if ev["changed"]:
                M_now[l - 1] = a
                depth[l] += 1
                cur[l] = newv
                last_new = newv
            W(0.4)

        # ------------------------- Zusammenfassung: Speicher / Laufzeit -------------------------
        left = [m for m in (band, mbox, s2, s1, hl) if m is not None]
        P(FadeOut(*left), last_new.animate.set_color(C_TEXT), t=0.8)
        summary = place_bl(VGroup(T("Speicher:  O(n)", 26, C_GREEN, weight=BOLD),
                                  T("Laufzeit:  O(n log n)", 26, C_GREEN, weight=BOLD)
                                  ).arrange(RIGHT, buff=0.9), Y_S1)
        P(FadeIn(summary, shift=UP * 0.1), t=0.8)
        W(1.5)

        # ------------------------- Rückverfolgen -------------------------
        note = place_bl(VGroup(
            T("Rückverfolgen benötigt Zusatzinformation:", 22, C_BLUE, weight=BOLD),
            T("speichere für jedes Array-Element den Vorgänger beim Eintragen.", 22, C_BLUE, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1), (Y_S2 + Y_S3) / 2)
        P(FadeIn(note, shift=UP * 0.1), t=0.9)
        W(0.8)

        def arc_arrow(j_from, j_to):
            """Bogen über dem Array von Element j_from zu seinem Vorgänger j_to."""
            top = Y_A + 0.375 + 0.06
            p = np.array([xa(j_from), top, 0.0])
            q = np.array([xa(j_to), top, 0.0])
            ar = CurvedArrow(p, q, angle=TAU / 6, color=C_BLUE, stroke_width=3.5)
            if ar.get_center()[1] < p[1]:      # falls der Bogen nach unten zeigt: spiegeln
                ar = CurvedArrow(p, q, angle=-TAU / 6, color=C_BLUE, stroke_width=3.5)
            return ar

        nodes = [T(str(A[j - 1]), 26, C_GREEN, weight=BOLD) for j in chain]
        seps = [None] + [T("→", 24, C_MUTED) for _ in chain[1:]]
        pieces = []
        for k, nd in enumerate(nodes):
            if seps[k] is not None:
                pieces.append(seps[k])
            pieces.append(nd)
        chain_txt = VGroup(*pieces).arrange(RIGHT, buff=0.2)
        if chain_txt.width > 4.6:
            chain_txt.scale_to_fit_width(4.6)
        chain_txt.move_to(np.array([2.3, Y_S1, 0.0]), aligned_edge=LEFT)

        def mark_cell(j):
            return a_cells[j].animate.set_fill(C_GREEN, opacity=GLOW).set_stroke(C_GREEN, width=3)

        P(mark_cell(chain[0]), FadeIn(nodes[0]), t=0.7)
        for k in range(1, len(chain)):
            P(Create(arc_arrow(chain[k - 1], chain[k])), mark_cell(chain[k]),
              FadeIn(seps[k]), FadeIn(nodes[k]), t=0.9)
            W(0.2)
        W(0.8)

        # Ergebnis: Teilfolge in aufsteigender Reihenfolge
        inc = []
        for k, j in enumerate(reversed(chain)):
            if k:
                inc.append(T("<", 24, C_MUTED))
            inc.append(T(str(A[j - 1]), 26, C_GREEN, weight=BOLD))
        inc_txt = VGroup(*inc).arrange(RIGHT, buff=0.2)
        if inc_txt.width > 4.6:
            inc_txt.scale_to_fit_width(4.6)
        inc_txt.move_to(np.array([2.3, Y_S1, 0.0]), aligned_edge=LEFT)
        P(FadeOut(*pieces), FadeIn(inc_txt, shift=UP * 0.1), t=1.0)
        W(3.0)
