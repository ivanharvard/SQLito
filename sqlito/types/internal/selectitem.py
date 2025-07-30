from sqlito.utils import store_as_storageclass

class SelectItem:
    def __init__(self, value, alias=None):
        if hasattr(value, 'evaluate'):
            self.value = value
        else:
            self.value = store_as_storageclass(value)
        self.alias = alias

    def evaluate(self, db):
        """
        Evaluate the value of the select item.
        
        :return: The evaluated value.
        """
        return self.value.evaluate(db)

    def __repr__(self):
        return f"SelectItem(value={self.value}, alias={self.alias})"