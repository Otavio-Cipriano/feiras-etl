from bs4 import BeautifulSoup


class HtmlCollector:
    def __init__(self, html):
        self._soup = BeautifulSoup(html, "html.parser")

    def select(self, selector):
        return self._soup.select(selector)

    def text(self, selector):
        elements = self.select(selector)
        return [e.get_text(strip=True) for e in elements]

    def link_href(self, link_text):
        link = self._soup.find("a", text=link_text)
        print(link)
        return link["href"]
