class EmptyTableException(Exception):
    def __init__(self):
        """
        Constructor for User defined exception raised when EmptyTable is read
        :return: EmptyTableException object
        """
        self.value = "Empty table"

    def __str__(self):
        """
        User defined exception raised when EmptyTable is read
        :return: EmptyTableException will be raised
        """
        return repr(self.value)
