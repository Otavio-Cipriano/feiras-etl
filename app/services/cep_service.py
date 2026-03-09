import requests


class CEPService:

    def __init__(self, data, base_url="https://viacep.com.br/ws/"):
        self.base_url = base_url
        self.data = data

    def request_cep(self, uf, cidade, endereco):
        endereco = self.limpa_endereco(endereco)
        response = requests.get(f"{self.base_url}{uf}/{cidade}/{endereco}/json/")
        self.data = response.json()

    def limpa_endereco(self, endereco):
        separadores = ["C/", "C /", "X/", "X /", "/"]
        for sep in separadores:
            if sep in endereco:
                return endereco.split(sep)[0].strip()
        return endereco

    def get_cep(self, uf, cidade, endereco):
        self.request_cep(uf, cidade, endereco)
        return self.data
