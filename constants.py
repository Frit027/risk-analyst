from enum import Enum


class StatusType(Enum):
    SATISFIED = 'удовлетворено'
    PARTIALLY_SATISFIED = 'удовлетворено частично'
    DENIED = 'отказано'
