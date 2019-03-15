import requests
from lxml import html

class CrawlerFiis:
    def __init__(self):
        self.url = 'https://fiis.com.br/indicadores-estendido/'

    def gettable(self):
        r = requests.get(self.url)
        html_page = r.content
        tree = html.fromstring(html_page)
        table = tree.xpath('//tbody/tr')
        return table

    def parserow(self, row):
        if 'tr' == row.tag:
            elements = row.xpath('.//td')
            return [self._format_number(self._extract_info(elem)) for elem in elements]
        return []

    def _extract_info(self, elem):
        text = elem.text
        if None == text:
            children = elem.xpath('.//a')
            elements = [child.text for child in children]
            try:
                text = elements[0]
            except:
                text = ''
        return text

    def _format_number(self, elem):
        try:
            n = float(elem.replace('R$','').replace('.','').replace(',','.'))
            return n
        except:
            return elem

class Fii:
    def __init__(self, values):
        self.code = values[0]
        self.price = values[1]
        self.shareholdersequity = values[2]
        self.equity = values[3]
        self.yield1 = values[4]
        self.yield12 = values[5]
        self.volsells = values[6]
        self.volequity = values[7]
        self.obs = values[8]

    def __str__(self):
        return "{}\t{}\t{}".format(\
        self.code,\
        self.price,\
        self.equity\
        )

    def  equityperc(self):
        return self.equity / self.price

    def yield1perc(self):
        return self.yield1 / self.price

    def yield12perc(self):
        return ((1.0 + self.yield1perc()) ** 12) - 1

if __name__ == '__main__':
    crawler = CrawlerFiis()
    table = crawler.gettable()

    for row in table:
        fii = Fii(crawler.parserow(row))
        print(fii.yield12perc())
