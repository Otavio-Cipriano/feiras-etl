import pandas as pd

from .transformer import Transformer


class SPTransformer(Transformer):
    def __init__(self, data, cep_service):
        super().__init__(
            staged_path="app/data/staged/sp",
            data=data,
            cep_service=cep_service,
        )

    def transform(self):
        latest = self._get_latest_file()
        if latest and not self._is_file_expired(latest):
            print(f"Using in stage in cache: {latest}")
            return pd.read_csv(latest)

        df = pd.read_excel(self.data)
        df.columns = (
            df.columns.str.replace(r"\s+", " ", regex=True)
            .str.replace("\xa0", "", regex=False)
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

        self._write_staged_data("sp_transform.csv", df)  # ✅ usa método da base
        print(df.head(3).to_string())
        return df
