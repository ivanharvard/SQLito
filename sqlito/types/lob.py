from sqlito.types.none import NONE

class BLOB(NONE):
    """Class representing a BLOB field in SQLito. Equivalent to NONE."""
    def __init__(self):
        super().__init__()