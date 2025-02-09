from manim import *
from manim_chemistry import *
from pathlib import Path

script_path = Path(__file__).absolute().parent
files_path = script_path / "element_files" 
elements_filename = files_path / "Elements.csv"


class MagnesiumAtomAnimation(Scene):
    def construct(self):
        title = Text("Magnesium Atom", font_size=32)
        title.to_edge(UP)

        atom_bohr = BohrAtom(e=12, p=12, n=14)
        atom_bohr.scale(0.5)
        atom_bohr.shift(3 * RIGHT)

        self.play(Write(title))
        self.add(
            MElementObject.from_csv_file_data(
                filename=elements_filename, atomic_number=12
            ).shift(3 * LEFT)
        )
        self.play(
            Rotate(
                atom_bohr,
                angle=2 * PI,
                about_point=atom_bohr.get_center(),
                rate_func=linear,
            ),
            run_time=3
        )

        self.wait(0.5)