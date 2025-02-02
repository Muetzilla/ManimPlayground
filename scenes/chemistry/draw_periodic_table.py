from pathlib import Path
from manim import *
from manim_chemistry import *
script_path = Path(__file__).absolute().parent
files_path = script_path / "element_files" 

class DrawPeriodicTable(Scene):
     def construct(self):
        self.add(PeriodicTable(data_file=files_path / "Elements.csv"))
