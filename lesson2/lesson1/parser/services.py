import data_client

# Задание
# 1. Найти все строки, которые включают заданное слово
# 2. Найти все строки, которые включают заданное слово + цена


class KufarService:
    data_client_imp = data_client.PostgresClient()

    def search_by_word(self, word):
        for el in self.data_client_imp.select_by_word(word):
            print(el)

    def search_by_word_and_price(self, word, price_from, price_to):
        for el in self.data_client_imp.select_by_word_and_price(word, price_from, price_to):
            print(el)


# KufarService().search_by_word('Минск')
KufarService().search_by_word_and_price('Минск', 1500, 2000)

