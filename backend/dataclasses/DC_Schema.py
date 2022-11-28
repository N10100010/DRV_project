from dataclasses import dataclass
from abc import abstractmethod

import logging
logger = logging.getLogger(__name__)


@dataclass
class DC_Schema:
    #  todo: will every entity have an ID?

    _id: str

    def __init__(self, _id: str):
        self._id = _id

        self.__post__init__()

    @abstractmethod
    def __post__init__(self):
        logger.debug(f"Check correctness of {type(self)} id: {self._id}")
