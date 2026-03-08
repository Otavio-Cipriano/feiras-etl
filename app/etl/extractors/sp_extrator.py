from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
from etl.extractors.extractor import Extractor


class SPExtractor(Extractor):

    def __init__(self, base_url=None):
        self.base_url = base_url
        self.data = []

    def extract(self):
        response = requests.get(
            self.base_url + "/web/seguranca_alimentar/w/noticias/294187"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        link = soup.find("a", text="Excel")
        csv_url = link["href"]
        print(csv_url)
        csv_response = requests.get(self.base_url + csv_url)
        file = BytesIO(csv_response.content)

        self.data = pd.read_excel(file)

    def get_data(self):
        return self.data

    def validate(self):
        return self.base_url is not None
