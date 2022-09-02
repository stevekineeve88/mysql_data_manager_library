from typing import List


class Result:
    """ Object for storing MySQL result information
    """

    def __init__(self, status: bool, message: str = "", data: List[any] = []):
        """ Constructor for Result
        Args:
            status (bool):      Status of MySQL query
            message (str):      Error message
            data (List[any]):   Data returned from SELECT query
        """
        self.__status: bool = status
        self.__message: str = message
        self.__data: List[any] = data
        self.__last_insert_id: int or None = None
        self.__affected_rows: int = 0

    def get_status(self) -> bool:
        """ Get status
        Returns:
            bool
        """
        return self.__status

    def get_message(self) -> str:
        """ Get message
        Returns:
            str
        """
        return self.__message

    def get_data(self) -> List[any]:
        """ Get data
        Returns:
            List[any]
        """
        return self.__data

    def set_last_insert_id(self, last_insert_id: int):
        """ Set last insert ID from INSERT statement
        Args:
            last_insert_id (int):
        """
        self.__last_insert_id = last_insert_id

    def get_last_insert_id(self) -> int or None:
        """ Get last insert ID from INSERT statement
        Returns:
            int or None
        """
        return self.__last_insert_id

    def set_affected_rows(self, affected_rows: int):
        """ Set affected rows of query
        Args:
            affected_rows (int):
        """
        self.__affected_rows = affected_rows

    def get_affected_rows(self) -> int:
        """ Get affected rows of query
        Returns:
            int
        """
        return self.__affected_rows
