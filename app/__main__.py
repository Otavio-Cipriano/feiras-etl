from .config import URLS, Sites
from .drivers import HttpRequester


def main():
    # print("Loading...")
    # sp_extractor = SPExtractor(URLS[Sites.SP_SITE])
    # sp_extractor.extract()
    # cep_service = CEPService()

    # sp_transformer = SPTransformer(sp_extractor.get_data(), cep_service)
    # sp_transformer.transform()

    http_requester = HttpRequester(
        url=f"{URLS.get(Sites.SP_SITE_B)}/web/seguranca_alimentar/w/feiras-livres-sp"
    )
    res = http_requester.request_from_page()
    print(res["text"])


if __name__ == "__main__":
    main()
