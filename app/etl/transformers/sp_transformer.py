from datetime import datetime, timezone

import pandas as pd

# TODO: Não criar stagged novamente, se não for tão antigo


class SPTransformer:
    def __init__(self, data, cep_service):
        self.data = data
        self.cep_service = cep_service

    def transform(self):
        df = pd.read_excel(self.data)
        df.columns = (
            df.columns.str.replace(r"\s+", " ", regex=True)  # normaliza espaços
            .str.replace("\xa0", "", regex=False)  # remove NBSP
            .str.strip()
        )
        df["NÚMERO"] = df["NÚMERO"].astype(str)
        df = df[
            [
                "CÓDIGO DE REGISTRO",
                "DIA DA SEMANA",
                "CATEGORIA",
                "QUANTIDADE DE FEIRANTES",
                "ENDEREÇO",
                "NÚMERO",
                "BAIRRO",
                "REFERÊNCIA",
                "SUBPREFEITURA",
            ]
        ]
        df = df.rename(
            columns={
                "CÓDIGO DE REGISTRO": "codigo_feira",
                "DIA DA SEMANA": "dia",
                "CATEGORIA": "categoria",
                "ENDEREÇO": "endereco",
                "NÚMERO": "numero",
                "REFERÊNCIA": "referencia",
                "QUANTIDADE DE FEIRANTES": "numero_feirantes",
                "BAIRRO": "bairro",
                "SUBPREFEITURA": "subprefeitura",
            }
        )
        df = df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)

        df = df.fillna("")

        # df = df.drop_duplicates(subset=["codigo_feira"])

        # colunas_obrigatorias = ["codigo_feira", "cep", "endereco", "dia", "categoria"]

        # vazios = df[df[colunas_obrigatorias].eq("").any(axis=1)]

        # for index, row in vazios.iterrows():
        #     if not row["cep"]:
        #         cep = self.cep_service.get_cep("SP", "Sao Paulo", row["endereco"])
        #         df.at[index, "cep"] = cep
        #         time.sleep(1)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", None)
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        df.to_csv(f"app/data/staged/{now}_sp_transform.csv", index=False)
        print(df.head(3).to_string())
