import os
from typing import Dict
import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql_data_manager.modules.connection.objects.result import Result


class ConnectionManager:
    """ Manager for MySQL queries that creates a connection pool and manages queries
    """

    def __init__(self, pool_name: str, pool_size: int = 3, **kwargs):
        """ Constructor for ConnectionManager
        Args:
            pool_name (str):        Arbitrary pool name
            pool_size (int):        How many connections inside of connection pool
            **kwargs:               Optional arguments
                host (str): DB host name
                port (int): DB port
                user (str): DB user
                pwd (str): DB password
                db (str): DB name
        """
        self.__host: str = kwargs.get("host") or os.environ["MYSQL_DB_HOST"]
        self.__port: int = kwargs.get("port") or int(os.environ["MYSQL_DB_PORT"])
        self.__user: str = kwargs.get("user") or os.environ["MYSQL_DB_USER"]
        self.__pwd: str = kwargs.get("pwd") or os.environ["MYSQL_DB_PWD"]
        self.__db: str = kwargs.get("db") or os.environ["MYSQL_DB_NAME"]

        self.__pool_name: str = pool_name
        self.__pool_size: int = pool_size

        self.__connection: PooledMySQLConnection = mysql.connector.connect(
            pool_name=self.__pool_name,
            pool_size=self.__pool_size,
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__pwd,
            database=self.__db
        )

    def get_host(self) -> str:
        """ Get host
        Returns:
            str
        """
        return self.__host

    def get_port(self) -> int:
        """ Get port
        Returns:
            int
        """
        return self.__port

    def get_user(self) -> str:
        """ Get user
        Returns:
            str
        """
        return self.__user

    def get_db_name(self) -> str:
        """ Get DB name
        Returns:
            str
        """
        return self.__db

    def get_pool_name(self) -> str:
        """ Get pool name
        Returns:
            str
        """
        return self.__pool_name

    def get_pool_size(self) -> int:
        """ Get pool size
        Returns:
            int
        """
        return self.__pool_size

    def get_connection(self) -> PooledMySQLConnection:
        """ Get connection pool
        Returns:
            PooledMySQLConnection
        """
        return self.__connection

    def select(self, sql: str, binding_params: Dict[str, any] = {}) -> Result:
        """ MySQL SELECT handler
        Args:
            sql (str):                              SQL statement
            binding_params (Dict[str, any]):        Binding parameters
        Returns:
            Result
        """
        cursor = self.__connection.cursor(dictionary=True)
        try:
            if len(binding_params) == 0:
                cursor.execute(sql)
            else:
                cursor.execute(sql, binding_params)
            return self.__build_result(Result(True, "", cursor.fetchall()),  cursor.rowcount)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    def insert(self, sql: str, binding_params: Dict[str, any] = {}) -> Result:
        """ MySQL INSERT handler
        Args:
            sql (str):                              SQL statement
            binding_params (Dict[str, any]):        Binding parameters
        Returns:
            Result
        """
        cursor = self.__connection.cursor()
        try:
            if len(binding_params) == 0:
                cursor.execute(sql)
            else:
                cursor.execute(sql, binding_params)
            return self.__build_result(Result(True), cursor.rowcount, cursor.lastrowid)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    def query(self, sql: str, binding_params: Dict[str, any] = {}) -> Result:
        """ MySQL INSERT handler
        Args:
            sql (str):                              SQL statement
            binding_params (Dict[str, any]):        Binding parameters
        Returns:
            Result
        """
        cursor = self.__connection.cursor()
        try:
            if len(binding_params) == 0:
                cursor.execute(sql)
            else:
                cursor.execute(sql, binding_params)
            return self.__build_result(Result(True), cursor.rowcount)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    @classmethod
    def __build_result(cls, result: Result, affect_rows: int = 0, last_insert_id: int or None = None) -> Result:
        """ Build Result object
        Args:
            result (Result):
            affect_rows (int):
            last_insert_id (int or None):
        Returns:
            Result
        """
        result.set_affected_rows(affect_rows)
        result.set_last_insert_id(last_insert_id)
        return result
