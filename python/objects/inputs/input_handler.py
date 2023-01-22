from abc import ABC, abstractmethod
from typing import List

from .inputs import Inputs


class InputHandler(ABC):
    @abstractmethod
    def get_latest_inputs(self) -> List[Inputs]:
        ...
