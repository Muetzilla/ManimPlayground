from pathlib import Path
from manim import *
from manim_chemistry import *
script_path = Path(__file__).absolute().parent
files_path = script_path / "element_files" 

class DrawSingleElement(Scene):

    def construct(self):
        self.add(
            MElementObject.from_csv_file_data(
                filename=files_path / "Elements.csv", atomic_number=6
            )
        )