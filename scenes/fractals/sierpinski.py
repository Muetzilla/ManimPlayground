from manim import *

class SierpinskiTriangle(Scene):
    def construct(self):
        main_triangle = Triangle().scale(4).set_fill(WHITE, opacity=1).set_stroke(width=0)
        self.add(main_triangle)  
        self.wait(1)

        depth = 5 
        self.sierpinski_recursive([main_triangle], depth)

        self.wait(3) 

    def sierpinski_recursive(self, triangles, depth):
        """ Erzeugt das Sierpiński-Dreieck mit simultaner Stufen-Animation """
        if depth == 0:
            return
        
        new_triangles = []  
        fade_in_objects = []  
        
        for triangle in triangles:
            p1, p2, p3 = triangle.get_vertices()

            mid1 = (p1 + p2) / 2
            mid2 = (p2 + p3) / 2
            mid3 = (p3 + p1) / 2

            middle_triangle = Polygon(mid1, mid2, mid3).set_fill(BLACK, opacity=1).set_stroke(width=0)

            tri1 = Polygon(p1, mid1, mid3).set_fill(WHITE, opacity=1).set_stroke(width=0)
            tri2 = Polygon(mid1, p2, mid2).set_fill(WHITE, opacity=1).set_stroke(width=0)
            tri3 = Polygon(mid3, mid2, p3).set_fill(WHITE, opacity=1).set_stroke(width=0)

            fade_in_objects.append(middle_triangle)  
            fade_in_objects.append(tri1)
            fade_in_objects.append(tri2)
            fade_in_objects.append(tri3)

            new_triangles.extend([tri1, tri2, tri3])  

        self.play(*[FadeIn(obj) for obj in fade_in_objects], run_time=0.5)

        self.sierpinski_recursive(new_triangles, depth - 1)
