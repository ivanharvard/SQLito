from .integer import IntegerStorage
from .null import NullStorage
from .real import RealStorage
from .text import TextStorage
from .blob import BlobStorage

STORAGECLASSES = (
    IntegerStorage,
    NullStorage,
    RealStorage,
    TextStorage,
    BlobStorage
)

__all__ = [
    "IntegerStorage",
    "NullStorage",
    "RealStorage",
    "TextStorage",
    "BlobStorage"
]