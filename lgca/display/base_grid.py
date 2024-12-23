from abc import abstractmethod
from copy import deepcopy
import pygame


class BaseGrid:

    @abstractmethod
    def set_up_window(self) -> None:
        """Needs to be implemented."""

    @abstractmethod
    def draw_grid(self) -> None:
        """Needs to be implemented."""

    def __init__(
        self,
        automaton,
        title: str = "Base Grid",
        tile_size: int = 1,
        run: bool = False,
        fps: int = 60,
        max_iteration: int = -1,
        colors: tuple = ("#000000", "#ffffff"),
        background: str | tuple[tuple[int, int, int]] = "#000000",
    ):
        self.title = title
        self.animate: bool = run
        self.automaton = automaton
        self.initial_grid_state = deepcopy(self.automaton.grid)
        self.fps = fps
        self.max_iteration = max_iteration
        self.tile_size = tile_size
        self.colors = colors
        self.background = background

        self.set_up_window()

    def __next__(self):
        if 0 < self.max_iteration < self.automaton.step:
            return

        self.draw_grid()

        if self.animate:
            next(self.automaton)

    def mainloop(self):
        pygame.init()
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_SPACE:
                            self.animate = not self.animate
                        case pygame.K_s:
                            self.automaton.grid = deepcopy(self.initial_grid_state)
                            self.automaton.step = 0
                        case pygame.K_RIGHT:
                            if not self.animate:
                                next(self.automaton)
            next(self)

            clock.tick(self.fps)
