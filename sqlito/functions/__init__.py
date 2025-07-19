from .abs import ABS
from .count import COUNT
from .max import MAX
from .min import MIN
from .sum import SUM

# tuple of all SQLito functions, useful for checking if a given function is a SQLito function
SQLITO_FUNCTIONS = (
    ABS,
    COUNT,
    MAX,
    MIN,
    SUM,
)

__all__ = [
    "ABS",
    "COUNT",
    "MAX",
    "MIN",
    "SUM",
    "SQLITO_FUNCTIONS",
]