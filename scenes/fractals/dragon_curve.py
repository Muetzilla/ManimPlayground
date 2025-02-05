from manim import *

class DragonCurve(Scene):
    def construct(self):
        self.camera.frame_height = 8

        iterations = 12

        start = np.array([-3, 0, 0])
        end = np.array([3, 0, 0])
        line = Line(start, end, color=BLUE)

        self.play(Create(line))
        self.wait(0.5)

        lines = [line]
        direction = 1  

        for _ in range(iterations):
            new_lines = []
            last_point = lines[0].get_start() 
            for l in lines:
                midpoint = (l.get_start() + l.get_end()) / 2
                direction_vector = l.get_end() - l.get_start()

                rotation_matrix = np.array([[0, -1], [1, 0]]) if direction == 1 else np.array([[0, 1], [-1, 0]])

                rotated_direction = np.dot(rotation_matrix, direction_vector[:2]) / 2
                new_midpoint = midpoint[:2] + rotated_direction

                left = Line(last_point, np.append(new_midpoint, 0), color=BLUE)
                right = Line(np.append(new_midpoint, 0), l.get_end(), color=BLUE)

                new_lines.extend([left, right])
                last_point = right.get_end()  
            self.play(
                *[Transform(old, new) for old, new in zip(lines, new_lines[: len(lines)])],
                *[Create(new) for new in new_lines[len(lines):]],
                run_time=1.2
            )
            lines = new_lines
            direction *= -1  
            self.wait(0.5)
