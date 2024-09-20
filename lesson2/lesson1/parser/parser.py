import requests
from bs4 import BeautifulSoup
import logging
import data_client1
import re
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

class Parser:
    links_to_parse = [
        'https://www.kufar.by/l/mebel',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6NH0%3D'
    ]
    data_client_imp = data_client1.PostgresClient()

    @staticmethod
    def get_mebel_by_link(link):
        try:
            response = requests.get(link)
            response.raise_for_status()
            mebel_data = response.text

            mebel_items = []
            to_parse = BeautifulSoup(mebel_data, 'html.parser')
            for elem in to_parse.find_all('a', class_='styles_wrapper__5FoK7'):
                try:
                    # Используем регулярное выражение для извлечения цены и описания
                    match = re.search(r'(\d[\d\s]*)\s*р\.\s*(.*)', elem.text)
                    if match:
                        price = int(match.group(1).replace(' ', ''))
                        description = match.group(2).strip()
                        mebel_items.append((
                            elem['href'],
                            price,
                            description
                        ))
                    else:
                        logging.warning(f'Не удалось извлечь цену и описание: {elem.text}')
                except Exception as e:
                    logging.error(f'Ошибка при обработке элемента: {e}')

            return mebel_items
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе к {link}: {e}")
            return []

    def save_to_postgres(self, mebel_items):
        try:
            self.data_client_imp.create_mebel_table()
            with self.data_client_imp as client:
                for item in mebel_items:
                    client.insert(item[0], item[1], item[2])
        except Exception as e:
            logging.error(f"Ошибка при сохранении данных в базу данных: {e}")

    def run(self):
        mebel_items = []
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.get_mebel_by_link, Parser.links_to_parse))
            for result in results:
                mebel_items.extend(result)
        self.save_to_postgres(mebel_items)

if __name__ == "__main__":
    Parser().run()