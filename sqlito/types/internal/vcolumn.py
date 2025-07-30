from dataclasses import dataclass
from typing import Optional

@dataclass
class VirtualColumn:
    data: list
    alias: Optional[str] = None

    def AS(self, alias: str):
        """
        Assign an alias to the virtual column.
        
        :param alias: The alias to assign to the virtual column.
        :type alias: str
        """
        self.alias = alias
        return self
    
    def evaluate(self, _db):
        return self.data

    def __getitem__(self, index):
        return self.data[index]
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return str(self.data)
    
