from sqlito._storageclass import BlobStorage

class SerializedBlobStorage(BlobStorage):
    def evaluate(self, _db=None):
        """
        Returns the de-serialized value of this storage class instance as a 
        single item list.

        :param _db: Database (not used in this context, ignored).
        :type _db: any

        :return: The de-serialized value stored in this instance.
        :rtype: list[any]
        """

        import pickle
        return [pickle.loads(self.value)]
