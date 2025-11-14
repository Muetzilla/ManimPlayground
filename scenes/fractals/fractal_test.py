from manim import *


class TriangeFractal(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        frame=self.camera.frame
        tri=Triangle()
        for i in range(7):
            triangle = VGroup(*[tri.copy() for _ in range(3)])
            triangle[1].next_to(triangle[0], RIGHT)
            new_t = VGroup(triangle[0], triangle[1])
            triangle[2].next_to(new_t, UP)
            self.play(frame.animate.move_to(triangle.get_center()).set_height(triangle.get_height()*1.5))
            self.play(Create(triangle))
            self.wait(1)
            tri=triangle