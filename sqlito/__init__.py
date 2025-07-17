def _set_version():
    """Set SQLito __version__"""
    # Thanks to check50 for the code!
    global __version__
    from importlib.metadata import PackageNotFoundError, version
    import os
    # https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
    try:
        __version__ = version("SQLito")
    except PackageNotFoundError:
        __version__ = "UNKNOWN"

_set_version()

from sqlito.database import Database
from sqlito.table import Table
from sqlito.query import Query
from sqlito.builders import TableBuilder, RowBuilder
from sqlito.utils import *
from sqlito.exceptions import SQLitoError, SQLitoTypeError, SQLitoValueError

__all__ = [
    "Database",
    "Table",
    "Query",
    "TableBuilder",
    "RowBuilder",
    "SQLitoError",
    "SQLitoTypeError",
    "SQLitoValueError"
]

