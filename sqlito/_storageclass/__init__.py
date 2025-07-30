from .integer import IntegerStorage
from .null import NullStorage
from .real import RealStorage
from .text import TextStorage
from .blob import BlobStorage
from .serializedblob import SerializedBlobStorage

STORAGECLASSES = (
    IntegerStorage,
    NullStorage,
    RealStorage,
    SerializedBlobStorage,
    TextStorage,
    BlobStorage
)

__all__ = [
    "IntegerStorage",
    "NullStorage",
    "RealStorage",
    "SerializedBlobStorage",
    "TextStorage",
    "BlobStorage"
]