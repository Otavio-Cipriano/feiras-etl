from etl.extractors.sp_extrator import SPExtractor
from etl.transformers.sp_transformer import SPTransformer


def main():
    print("Loading...")
    sp_extractor = SPExtractor("https://prefeitura.sp.gov.br")
    sp_extractor.extract()
    # cep_service = CEPService()

    sp_transformer = SPTransformer(sp_extractor.get_data())
    sp_transformer.transform()


if __name__ == "__main__":
    main()
