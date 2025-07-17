class RANDOM:
    def __init__(self):
        """
        Initializes the RANDOM function.
        
        This function does not take any arguments.
        """
        self.name = "RANDOM"

    def to_sql(self):
        """
        Converts the RANDOM function to its SQL representation.
        
        :return: SQL representation of the RANDOM function.
        :rtype: str
        """
        return str(self)

    def __str__(self):
        """
        Returns the string representation of the RANDOM function.
        
        :return: String representation of the RANDOM function.
        :rtype: str
        """
        return f"{self.name}()"
    
    def __call__(self):
        """
        Generates a random integer value between -2^63 and 2^63 - 1, 
        inclusive. Uses the `secrets` module for cryptographic randomness.
        
        :return: A random integer value between -2^63 and 2^63 - 1.
        :rtype: int
        """
        import secrets 

        # Generates a number between 0 and 2**64 - 1
        unsigned = secrets.randbits(64)
        # Convert to signed 64-bit integer
        return unsigned if unsigned < 2**63 else unsigned - 2**64