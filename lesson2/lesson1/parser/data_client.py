import sqlite3
from sqlite3 import Error
# pip install psycopg2
import psycopg2
from abc import ABC, abstractmethod


class DataClient(ABC):
    @abstractmethod
    def _get_connection(self):
        pass

    @abstractmethod
    def create_mebel_table(self):
        pass

    @abstractmethod
    def get_items(self, price_from=0, price_to=100000):
        pass

    @abstractmethod
    def insert(self, link, price, description):
        pass

    @abstractmethod
    def select_by_word(self, word):
        pass

    @abstractmethod
    def select_by_word_and_price(self, word, price_from, price_to):
        pass

    def run_test(self):
        self.create_mebel_table()
        items = self.get_items(price_from=10, price_to=30)
        for item in items:
            print(item)


class PostgresClient(DataClient):
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5433"

    def _get_connection(self):
        return psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
        )

    def select_by_word(self, word):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_1_mebel WHERE description LIKE '%s'", (word, ))
            return cursor.fetchall()

    def select_by_word_and_price(self, word, price_from, price_to):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM app_1_mebel WHERE description LIKE %s and price >= %s and price <= %s",
                (f'%{word}%', price_from, price_to)
            )
            return cursor.fetchall()

    def create_mebel_table(self):
        with self._get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(
                """
                    CREATE TABLE IF NOT EXISTS app_1_mebel
                    (
                        id serial PRIMARY KEY, 
                        link text, 
                        price integer, 
                        description text
                    )
                """
            )

    def get_items(self, price_from=0, price_to=100000):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
            return cursor.fetchall()

    def insert(self, link, price, description):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO app_1_mebel (link, price, description) VALUES ('{link}', '{float(price)}', '{description}')")
            conn.commit()


class Sqlite3Client(DataClient):
    DB_NAME = "kufar.db"

    def select_by_word(self, word):
        pass

    def select_by_word_and_price(self, word, price_from, price_to):
        pass

    def _get_connection(self):
        return sqlite3.connect(self.DB_NAME)

    def create_mebel_table(self):
        with self._get_connection() as conn:
            cursor_object = conn.cursor()
            cursor_object.execute(
                """
                    CREATE TABLE IF NOT EXISTS app_1_mebel
                    (
                        id integer PRIMARY KEY autoincrement, 
                        link text, 
                        price integer, 
                        description text
                    )
                """
            )

    def get_items(self, price_from=0, price_to=100000):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}')
            return cursor.fetchall()

    def insert(self, link, price, description):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO app_1_mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')")
            conn.commit()

# data_client = PostgresClient()
# data_client = Sqlite3Client()
# data_client.run_test()
