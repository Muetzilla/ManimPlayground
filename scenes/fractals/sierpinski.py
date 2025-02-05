from manim import *

class SierpinskiTriangle(Scene):
    def construct(self):
        self.camera.background_color = BLACK  # Schwarzer Hintergrund

        # Hauptdreieck (Basis)
        main_triangle = Triangle().scale(4).set_fill(WHITE, opacity=1).set_stroke(width=0)
        self.add(main_triangle)  # Direktes Hinzufügen des Startdreiecks
        self.wait(1)

        # Starte die rekursive Erzeugung mit gleichzeitiger Animation pro Stufe
        depth = 5  # Anzahl der Iterationen
        self.sierpinski_recursive([main_triangle], depth)

        self.wait(3)  # Wartezeit am Ende

    def sierpinski_recursive(self, triangles, depth):
        """ Erzeugt das Sierpiński-Dreieck mit simultaner Stufen-Animation """
        if depth == 0:
            return
        
        new_triangles = []  # Neue Dreiecke für die nächste Rekursionsebene
        fade_in_objects = []  # Elemente für gleichzeitige Einblendung
        
        for triangle in triangles:
            p1, p2, p3 = triangle.get_vertices()

            # Berechnung der Mittelpunkte
            mid1 = (p1 + p2) / 2
            mid2 = (p2 + p3) / 2
            mid3 = (p3 + p1) / 2

            # Schwarzes Mitteldreieck
            middle_triangle = Polygon(mid1, mid2, mid3).set_fill(BLACK, opacity=1).set_stroke(width=0)

            # Drei neue weiße Dreiecke
            tri1 = Polygon(p1, mid1, mid3).set_fill(WHITE, opacity=1).set_stroke(width=0)
            tri2 = Polygon(mid1, p2, mid2).set_fill(WHITE, opacity=1).set_stroke(width=0)
            tri3 = Polygon(mid3, mid2, p3).set_fill(WHITE, opacity=1).set_stroke(width=0)

            fade_in_objects.append(middle_triangle)  # Schwarzes Dreieck zum Entfernen
            fade_in_objects.append(tri1)
            fade_in_objects.append(tri2)
            fade_in_objects.append(tri3)

            new_triangles.extend([tri1, tri2, tri3])  # Speichern für die nächste Stufe

        # Jetzt alle Dreiecke einer Stufe gleichzeitig animieren
        self.play(*[FadeIn(obj) for obj in fade_in_objects], run_time=0.5)

        # Nächste Rekursionsstufe aufrufen
        self.sierpinski_recursive(new_triangles, depth - 1)
