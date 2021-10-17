from enum import Enum


class SolutionType(Enum):
    SATISFIED = 'удовлетворено'
    PARTIALLY_SATISFIED = 'удовлетворено частично'
    DENIED = 'не удовлетворено'
