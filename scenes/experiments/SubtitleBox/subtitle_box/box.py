from manim import *

class SubtitleBox(VGroup):
    def __init__(self, content="", box_height=1.0, is_latex=False, **kwargs):
        super().__init__(**kwargs)

        box_width = config.frame_width - 0.6

        self.rect = Rectangle(
            width=box_width,
            height=box_height,
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=2,
        )
        self.rect.to_edge(DOWN, buff=0.5)

        if is_latex:
            self.content_mobj = MathTex(
                content,
                font_size=32,
                color=WHITE,
            )
        else:
            self.content_mobj = Text(
                content,
                font_size=32,
                color=WHITE,
            )

        self.content_mobj.move_to(self.rect.get_center())
        self.add(self.rect, self.content_mobj)

    def set_content(self, new_content, is_latex=False):
        if is_latex:
            new_mobj = MathTex(
                new_content,
                font_size=32,
                color=WHITE,
            )
        else:
            new_mobj = Text(
                new_content,
                font_size=32,
                color=WHITE,
            )
        new_mobj.move_to(self.rect.get_center())
        return Transform(self.content_mobj, new_mobj)

    def set_text(self, txt):
        """Bequemer Alias für normalen Text."""
        return self.set_content(txt, is_latex=False)
