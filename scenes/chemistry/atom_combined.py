from manim import *
from manim_chemistry import *
from pathlib import Path
from manim.utils.tex_templates import TexTemplate


script_path = Path(__file__).absolute().parent
files_path = script_path / "element_files" 
elements_filename = files_path / "Elements.csv"


tex_template = TexTemplate()
tex_template.add_to_preamble(r"\usepackage{mhchem}")


class MagnesiumAtomAnimation(Scene):
    def construct(self):
        title = Tex(r"\ce{Magnesium Element}", tex_template=tex_template)
        title.to_edge(UP)

        atom_bohr = BohrAtom(e=12, p=12, n=14)
        atom_bohr.scale(0.5)
        atom_bohr.shift(3 * RIGHT)
        atom_center = atom_bohr.get_center()

        atom_information = MElementObject.from_csv_file_data(filename=elements_filename, atomic_number=12)
        atom_information.shift(3 * LEFT).scale(0.5)
        atom_information.set_stroke(width=0)

        self.play(Write(title))
        self.add(atom_information)
        self.add(atom_bohr)
        self.play(
            Rotate(
                atom_bohr,
                angle=2 * PI,
                about_point=atom_center,
                rate_func=linear,
            ),
            run_time=3
        )
        self.wait(1)