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
    def drawSingleWholeElement(self, atomName, atomElectron, atomProton, atomNeutron):
        title = Tex(r"\ce{"+ atomName+"}", tex_template=tex_template)
        title.to_edge(UP)

        atom_bohr = BohrAtom(e=atomElectron, p=atomProton, n=atomNeutron)
        atom_bohr.scale(0.5)
        atom_bohr.shift(3 * RIGHT)
        atom_center = atom_bohr.get_center()

        atom_information = MElementObject.from_csv_file_data(filename=elements_filename, atomic_number=atomElectron)
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
        self.wait(0.5)

    def construct(self):
        elements = [
            {"name": "Magnesium", "electrons": 12, "protons": 12, "neutrons": 14},
            {"name": "Sodium", "electrons": 11, "protons": 11, "neutrons": 12},
            {"name": "Oxygen", "electrons": 8, "protons": 8, "neutrons": 8},
            {"name": "Carbon", "electrons": 6, "protons": 6, "neutrons": 6},
            {"name": "Hydrogen", "electrons": 1, "protons": 1, "neutrons": 0},
            {"name": "Nitrogen", "electrons": 7, "protons": 7, "neutrons": 7},
            #{"name": "Calcium", "electrons": 20, "protons": 20, "neutrons": 20},
            #{"name": "Iron", "electrons": 26, "protons": 26, "neutrons": 30},
            #{"name": "Copper", "electrons": 29, "protons": 29, "neutrons": 35},
            #{"name": "Zinc", "electrons": 30, "protons": 30, "neutrons": 35},
            #{"name": "Silver", "electrons": 47, "protons": 47, "neutrons": 61},
        ]
        
        for element in elements:
            self.drawSingleWholeElement(
                element["name"], 
                element["electrons"], 
                element["protons"], 
                element["neutrons"]
            )
            if element != elements[-1]:
                self.play(FadeOut(*self.mobjects))
                self.wait(0.5)
                self.play(FadeIn(*self.mobjects))

