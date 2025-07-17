from sqlito.types.numeric import NUMERIC

class DATE(NUMERIC):
    """Class representing a DATE field in SQLito. Equivalent to NUMERIC."""
    def __init__(self):
        super().__init__()

class DATETIME(NUMERIC):
    """Class representing a DATETIME field in SQLito. Equivalent to NUMERIC."""
    def __init__(self):
        super().__init__()

class TIMESTAMP(NUMERIC):
    """Class representing a TIMESTAMP field in SQLito. Equivalent to NUMERIC."""
    def __init__(self):
        super().__init__()

class TIME(NUMERIC):
    """Class representing a TIME field in SQLito. Equivalent to NUMERIC."""
    def __init__(self):
        super().__init__()
