from pygame import Surface
from pygame.font import Font


class Text(Font):
    def __init__(
        self,
        text: str,
        font_size: int = 30,
        font_color: tuple[int, int, int] | None = None,
    ) -> None:
        super().__init__(None, font_size)
        self.__font_color = font_color or (255, 255, 255)
        self.__text = text

    def draw(self, surface: Surface, topleft: tuple[int, int] | None) -> None:
        text_surface = self.render(self.__text, 0, self.__font_color)
        if topleft is None:
            topleft = (
                surface.get_width() // 2 - text_surface.get_width() // 2,
                surface.get_height() // 2,
            )

        surface.blit(text_surface, topleft)

    def get_text_surface(self) -> Surface:
        return self.render(self.__text, 0, self.__font_color)
