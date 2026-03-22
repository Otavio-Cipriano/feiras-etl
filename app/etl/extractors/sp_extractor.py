from io import BytesIO

from app.config.urls import URLS, Sites
from app.drivers.html_collector import HtmlCollector
from app.drivers.http_requester import HttpRequester
from app.etl.extractors.extractor import Extractor

ENDPOINTS = {
    "main": f"{URLS.get(Sites.SP_SITE_B)}/web/seguranca_alimentar/w/feiras-livres-sp"
}


class SPExtractor(Extractor):

    def extract(self):
        latest_file = self._get_latest_file()

        if latest_file and not self._is_file_expired(latest_file):
            print("Using cached file")
            self.data = BytesIO(latest_file.read_bytes())
            return

        print("Downloading new file")
        http_requester = HttpRequester(ENDPOINTS.get("main"))
        response = http_requester.request_from_page()

        if response["status_code"] != 200:
            raise Exception(f"Error {response.status_code}")
        soup = HtmlCollector(response["text"])
        csv_url = soup.link_href("Excel")
        csv_response = http_requester.request_from_page(f"{self.base_url}/{csv_url}")
        self.data = self._write_new_raw_data(
            "sp", "sp_raw_data.xlsx", csv_response.content
        )
