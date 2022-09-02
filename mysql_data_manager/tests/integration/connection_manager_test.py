import os
import unittest
from mysql.connector.pooling import PooledMySQLConnection
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from dotenv import load_dotenv


class ConnectionManagerTest(unittest.TestCase):

    pool_name = "my_pool_name"
    pool_size = 3
    connection_manager: ConnectionManager or None = None

    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()

        cls.connection_manager = ConnectionManager(cls.pool_name, cls.pool_size)

        result = cls.connection_manager.query(f"""
            CREATE TABLE IF NOT EXISTS fake_table (
                id INT NOT NULL AUTO_INCREMENT,
                fake_column VARCHAR(255),
                PRIMARY KEY (`id`)
            )
        """)
        if not result.get_status():
            raise Exception(f"Initialization of tests failed: {result.get_message()}")

    def test_get_pool_name_gets_pool_name(self):
        self.assertEqual(self.pool_name, self.connection_manager.get_pool_name())

    def test_get_pool_size_gets_pool_size(self):
        self.assertEqual(self.pool_size, self.connection_manager.get_pool_size())

    def test_get_host_gets_host(self):
        self.assertEqual(os.environ["MYSQL_DB_HOST"], self.connection_manager.get_host())

    def test_get_port_gets_port(self):
        self.assertEqual(int(os.environ["MYSQL_DB_PORT"]), self.connection_manager.get_port())

    def test_get_user_gets_user(self):
        self.assertEqual(os.environ["MYSQL_DB_USER"], self.connection_manager.get_user())

    def test_get_db_name_gets_db_name(self):
        self.assertEqual(os.environ["MYSQL_DB_NAME"], self.connection_manager.get_db_name())

    def test_get_connection_returns_connection_pool_type(self):
        self.assertEqual(PooledMySQLConnection, type(self.connection_manager.get_connection()))

    def test_insert_and_select_returns_success_with_correct_information(self):
        fake_value = "Some Value"

        insert_result = self.connection_manager.insert(f"""
            INSERT INTO fake_table (fake_column)
            VALUES (%(fake_value)s)
        """, {
            "fake_value": fake_value
        })

        select_result = self.connection_manager.select(f"""
            SELECT id FROM fake_table WHERE fake_column = %(fake_value)s
        """, {
            "fake_value": fake_value
        })

        self.assertEqual(1, select_result.get_affected_rows())
        self.assertEqual(None, select_result.get_last_insert_id())

        self.assertTrue(insert_result.get_status())
        self.assertEqual(select_result.get_data()[0]["id"], insert_result.get_last_insert_id())
        self.assertEqual(1, insert_result.get_affected_rows())

    def test_insert_returns_failure_with_sql_syntax_error(self):
        result = self.connection_manager.insert(f"""
            INSERT INTO fake_take (wrong_column)
            VALUES ("some value")
        """)

        self.assertFalse(result.get_status())
        self.assertNotEqual("", result.get_message())
        self.assertEqual(None, result.get_last_insert_id())
        self.assertEqual(0, result.get_affected_rows())

    def test_select_returns_failure_with_sql_syntax_error(self):
        result = self.connection_manager.select(f"""
            SELECT * FROM wrong_table
        """)

        self.assertFalse(result.get_status())
        self.assertNotEqual("", result.get_message())
        self.assertEqual(0, len(result.get_data()))

    def test_query_returns_failure_with_sql_syntax_error(self):
        result = self.connection_manager.query(f"""
            TRUNCATE wrong_table
        """)

        self.assertFalse(result.get_status())
        self.assertNotEqual("", result.get_message())
        self.assertEqual(0, len(result.get_data()))

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            TRUNCATE fake_table
        """)

        if not result.get_status():
            raise Exception(f"Teardown of test instance failed: {result.get_message()}")

    @classmethod
    def tearDownClass(cls) -> None:
        result = cls.connection_manager.query(f"""
            DROP TABLE fake_table
        """)
        if not result.get_status():
            raise Exception(f"Teardown of tests failed: {result.get_message()}")
