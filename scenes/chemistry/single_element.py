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


class DrawSingleElemntFromPeriodicTable(Scene):
    def constructor(self):
        periodic_table = PeriodicTable(data_file=elements_filename)
        iron_element = periodic_table.get_element("Fe")
        self.add(periodic_table)

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

class CombineElements(Scene):
    def construct(self):
        element1 = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=12
        )
        
        element2 = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=8
        )

        fused_element = MElementObject.from_csv_file_data(
            filename=elements_filename, atomic_number=20
        )  

        element1.shift(LEFT * 3 + UP * 2)
        element2.shift(LEFT * 3 + DOWN * 2)
        fused_element.shift(RIGHT * 3)

        self.add(element1, element2)

        arrow1 = Arrow(start=element1.get_right(), end=fused_element.get_left(), buff=0.2)
        arrow2 = Arrow(start=element2.get_right(), end=fused_element.get_left(), buff=0.2)

        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            run_time=1
        )

        self.play(
            FadeIn(fused_element),
            run_time=2
        )

        self.wait(2)
