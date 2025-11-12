# main.py
from manim import *
from structure import ScriptedScene
from scripts.selection_sort import SCRIPT as SELECTION_SCRIPT
from visuals.selection_sort import Visuals as SelectionVisuals

class SelectionSortScene(ScriptedScene):
    SCRIPT = SELECTION_SCRIPT
    VISUALS_CLS = SelectionVisuals

__all__ = ["SelectionSortScene"]
