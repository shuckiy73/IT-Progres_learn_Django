import data_client
import logging

logging.basicConfig(level=logging.INFO)

class KufarService:
    data_client_imp = data_client.PostgresClient()

    def search_by_word(self, word):
        try:
            self.data_client_imp.connect()  # Открываем соединение с базой данных
            results = self.data_client_imp.select_by_word(word)
            for el in results:
                logging.info(el)
        except Exception as e:
            logging.error(f"Ошибка при поиске по слову '{word}': {e}")
        finally:
            self.data_client_imp.close()  # Закрываем соединение с базой данных

    def search_by_word_and_price(self, word, price_from, price_to):
        try:
            if price_from > price_to:
                raise ValueError("Значение 'price_from' должно быть меньше или равно 'price_to'")
            self.data_client_imp.connect()  # Открываем соединение с базой данных
            results = self.data_client_imp.select_by_word_and_price(word, price_from, price_to)
            for el in results:
                logging.info(el)
        except ValueError as ve:
            logging.error(f"Ошибка входных данных: {ve}")
        except Exception as e:
            logging.error(f"Ошибка при поиске по слову '{word}' и цене от {price_from} до {price_to}: {e}")
        finally:
            self.data_client_imp.close()  # Закрываем соединение с базой данных

# Пример использования
# KufarService().search_by_word('Минск')
KufarService().search_by_word_and_price('Минск', 1500, 2000)