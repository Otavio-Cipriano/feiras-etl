class SPTransformer:
    def __init__(self, data):
        self.data = data

    def transform(self):
        df = self.data
        df = df.rename(
            columns={
                "N.Feira": "codigo_feira",
                "Dia da semana": "dia",
                "Categoria": "categoria",
                "Endereço": "endereco",
                "Numero": "numero",
                "Referencia p/ localizacao": "referencia",
                "Bairro": "bairro",
                "CEP": "cep",
                "SUB-PREF.": "subprefeitura",
            }
        )
        df = df.fillna("")
        self.data = df
        return df
