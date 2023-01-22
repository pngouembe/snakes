import logging
import sys
from typing import List

import pygame

from .input_handler import InputHandler
from .inputs import Inputs

log = logging.getLogger(__package__)


# TODO: Setup the callbacks and make this a Thread
class PygameKeyboardHandler(InputHandler):
    def __init__(self) -> None:

        if not pygame.get_init():
            pygame.init()

        self.key_mapping = {
            pygame.K_UP: Inputs.UP,
            pygame.K_RIGHT: Inputs.RIGHT,
            pygame.K_DOWN: Inputs.DOWN,
            pygame.K_LEFT: Inputs.LEFT,
            pygame.K_SPACE: Inputs.PAUSE,
            pygame.K_ESCAPE: Inputs.QUIT
        }

    def get_latest_inputs(self) -> List[Inputs]:
        input_list = list()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info(f"Quitting the game!")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in self.key_mapping:
                    input_list.append(self.key_mapping[event.key])

        if input_list:
            log.debug(f"Registered the following entries: {input_list}")

        return input_list
