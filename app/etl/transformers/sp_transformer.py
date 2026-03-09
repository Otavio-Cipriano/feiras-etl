import pandas as pd


class SPTransformer:
    def __init__(self, data):
        self.data = data

    def transform(self):
        df = pd.read_excel(self.data)
        df.columns = df.columns.str.strip()
        df["Endereco"] = df.iloc[:, 3].str.strip() + " " + df["Endereco"].str.strip()
        df["Numero"] = df["Numero"].str.strip()
        df = df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)
        df = df.drop(columns=["Unnamed: 3"])
        df = df.rename(
            columns={
                "N.Feira": "codigo_feira",
                "Dia da semana": "dia",
                "Categoria": "categoria",
                "Endereco": "endereco",
                "Numero": "numero",
                "Referencia p/ localizacao": "referencia",
                "Bairro": "bairro",
                "CEP": "cep",
                "SUB-PREF.": "subprefeitura",
            }
        )
        df = df.fillna("")
        df = df.drop_duplicates(subset=["codigo_feira"])
        df = df.drop_duplicates(subset=["cep"])
        # colunas_obrigatorias = ["codigo_feira", "cep", "endereco", "dia", "categoria"]

        # vazios = df[df[colunas_obrigatorias].eq("").any(axis=1)]
        # for index, row in vazios.iterrows():
        #     if row["cep"] == 0:
        #         cep = self.cep_service.get_cep("SP", "Sao Paulo", row["endereco"])
        #         df.at[index, "cep"] = cep
        # print(vazios)

        print(df.head(20))
        self.data = df
