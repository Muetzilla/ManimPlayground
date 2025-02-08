from pathlib import Path
from manim import *
from manim_chemistry import *
script_path = Path(__file__).absolute().parent
files_path = script_path / "element_files" 
elements_filename = files_path / "Elements.csv"

class DrawSingleElement(Scene):

    def construct(self):
        self.add(
            MElementObject.from_csv_file_data(
                filename=elements_filename, atomic_number=26
            )
        )

class DrawMagnesium(Scene):

    def construct(self):
        self.add(
            MElementObject.from_csv_file_data(
                filename=elements_filename, atomic_number=12
            )
        )

class DrawTwoElements(Scene):
    def construct(self):
        magnesium_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=12
        )
        
        oxygen_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=8
        )

        magnesium_element.shift(LEFT * 2)
        oxygen_element.shift(RIGHT * 2)

        self.add(magnesium_element, oxygen_element)

        self.play(
            oxygen_element.animate.shift(UP * 2),
            magnesium_element.animate.shift(UP * 2),
            run_time=2
        )


        self.wait(2)

class DrawMultipleElements(Scene):
    def construct(self):
        magnesium_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=12
        )
        
        oxygen_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=8
        )

        iron_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=26
        )

        magnesium_element.shift(LEFT * 2)
        oxygen_element.shift(RIGHT * 2)

        self.add(magnesium_element, oxygen_element,iron_element)

        self.play(
            oxygen_element.animate.shift(UP * 2),
            magnesium_element.animate.shift(UP * 2),
            run_time=2
        )


        self.wait(2)

