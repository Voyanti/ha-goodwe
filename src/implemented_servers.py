from enum import Enum

from .goodwe_gt import GoodweGT
from src.goodwe_ht import GoodweHT
from .goodwe_logger import GoodweLogger


class ServerTypes(Enum):
    GOODWE_LOGGER = GoodweLogger
    GOODWE_GT = GoodweGT
    GOODWE_HT = GoodweHT