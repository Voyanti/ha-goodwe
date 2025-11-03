from enum import Enum

from .goodwe_gt import GoodweGT
from .goodwe_logger import GoodweLogger


class ServerTypes(Enum):
    GOODWE_LOGGER = GoodweLogger
    GOODWE_GT = GoodweGT