from app.config import URLS, Sites
from app.etl.extractors.sp_extractor import SPExtractor
from app.etl.transformers.sp_transformer import SPTransformer
from app.services.cep_service import CEPService


class SpPipeline:
    @staticmethod
    def run():
        print("Loading...")
        sp_extractor = SPExtractor("sp", URLS[Sites.SP_SITE])
        sp_extractor.extract()
        cep_service = CEPService()

        sp_transformer = SPTransformer(sp_extractor.get_data(), cep_service)
        sp_transformer.transform()
