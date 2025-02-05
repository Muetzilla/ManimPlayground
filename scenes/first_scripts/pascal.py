from manim import *

class PascalsTriangle(Scene):
    def construct(self):
        self.camera.background_color = WHITE 
        rows = 7 
        triangle = self.generate_pascals_triangle(rows)

        for row in triangle:
            self.play(*[FadeIn(num) for num in row], run_time=1)
            self.wait(0.5) 
        
        self.wait(2)

    def generate_pascals_triangle(self, num_rows):
        triangle = []
        values = [[1]]

        for i in range(1, num_rows):
            row = [1]
            for j in range(len(values[i - 1]) - 1):
                row.append(values[i - 1][j] + values[i - 1][j + 1])
            row.append(1)
            values.append(row)

        for i, row in enumerate(values):
            row_objects = []
            for j, num in enumerate(row):
                text = Text(str(num), font_size=36, color=BLACK)
                text.move_to(DOWN * i + RIGHT * (j - len(row) / 2)) 
                row_objects.append(text)
            triangle.append(row_objects)

        return triangle
