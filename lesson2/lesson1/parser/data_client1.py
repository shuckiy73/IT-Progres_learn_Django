import psycopg2

class PostgresClient:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="your_dbname",
                user="your_username",
                password="your_password",
                host="your_host",
                port="your_port"
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

    def select_by_word(self, word):
        query = f"SELECT * FROM your_table WHERE description ILIKE '%{word}%';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_by_word_and_price(self, word, price_from, price_to):
        query = f"SELECT * FROM your_table WHERE description ILIKE '%{word}%' AND price BETWEEN {price_from} AND {price_to};"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()