import time
from datetime import datetime, timezone

import pandas as pd


class SPTransformer:
    def __init__(self, data, cep_service):
        self.data = data
        self.cep_service = cep_service

    def transform(self):
        df = pd.read_excel(self.data)
        df["Numero"] = df["Numero"].astype(str).str.strip()
        df.columns = df.columns.str.strip()
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
        df = df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)

        df["endereco"] = df["Unnamed: 3"].str.strip() + " " + df["endereco"]

        df = df.drop(columns=["Unnamed: 3"])

        df = df.fillna("")

        df = df.drop_duplicates(subset=["codigo_feira"])

        colunas_obrigatorias = ["codigo_feira", "cep", "endereco", "dia", "categoria"]

        vazios = df[df[colunas_obrigatorias].eq("").any(axis=1)]

        for index, row in vazios.iterrows():
            if not row["cep"]:
                cep = self.cep_service.get_cep("SP", "Sao Paulo", row["endereco"])
                df.at[index, "cep"] = cep
                time.sleep(1)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", None)
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        df.to_csv(f"app/data/stagged/{now}_sp_transform.csv", index=False)
        print(df.head(3).to_string())
