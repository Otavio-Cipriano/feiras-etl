from typing import Dict

import requests


class HttpRequester:
    def __init__(self, url):
        print(url)
        self.__url = url

    def request_from_page(self) -> Dict[int, str]:
        if not self.__valid():
            raise ValueError("URL inválida")

        res = requests.get(self.__url)

        return {"status_code": res.status_code, "text": res.text}

    def __valid(self):
        return self.__url is not None
