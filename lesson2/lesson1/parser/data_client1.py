import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

class PostgresClient:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="app_1_mebel",
                USER = "postgres",
                PASSWORD = "postgres",
                HOST = "localhost",
                PORT = "5433"
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            logging.error(f"Ошибка при подключении к базе данных: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_mebel_table(self):
        if not self.cursor:
            logging.error("Курсор не инициализирован")
            return
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS mebel (
                id SERIAL PRIMARY KEY,
                link TEXT NOT NULL,
                price INTEGER NOT NULL,
                description TEXT NOT NULL
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except psycopg2.Error as e:
            logging.error(f"Ошибка при создании таблицы 'mebel': {e}")
            raise

    def select_by_word(self, word):
        if not self.cursor:
            logging.error("Курсор не инициализирован")
            return []
        query = f"SELECT * FROM mebel WHERE description ILIKE '%{word}%';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_by_word_and_price(self, word, price_from, price_to):
        if not self.cursor:
            logging.error("Курсор не инициализирован")
            return []
        query = f"SELECT * FROM mebel WHERE description ILIKE '%{word}%' AND price BETWEEN {price_from} AND {price_to};"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class KufarService:
    def __init__(self):
        self.data_client_imp = PostgresClient()

    def search_by_word(self, word):
        with self.data_client_imp as client:
            try:
                results = client.select_by_word(word)
                for el in results:
                    logging.info(el)
            except Exception as e:
                logging.error(f"Ошибка при поиске по слову '{word}': {e}")

    def search_by_word_and_price(self, word, price_from, price_to):
        if price_from > price_to:
            logging.error("Значение 'price_from' должно быть меньше или равно 'price_to'")
            return

        with self.data_client_imp as client:
            try:
                results = client.select_by_word_and_price(word, price_from, price_to)
                for el in results:
                    logging.info(el)
            except Exception as e:
                logging.error(f"Ошибка при поиске по слову '{word}' и цене от {price_from} до {price_to}: {e}")

# Пример использования
# KufarService().search_by_word('Минск')
KufarService().search_by_word_and_price('Минск', 1500, 2000)