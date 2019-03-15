import requests
import time
from os import path
from os import stat
from lxml import html

class CrawlerClubeFii:
    def __init__(self):
        self.url = 'https://www.clubefii.com.br/proventos-rendimento-distribuicoes-amortizacoes_ajx?verifica_ultimo_provento=false'

    def load_fiis(self):
        filename = 'html.cache'
        html = ''
        if path.isfile(filename):
            # time since last modification in minutes should be less than 1 hour
            if (time.time() - stat(filename).st_mtime) / 60 > 60:
                html = self.request_html(url)
                self.save_html(html)
            else:
                html = self.load_html()
        else:
            html = self.request_html(self.url)
            self.save_html(str(html))
        return html

    def fake_load_fiis(self):
        html = self.load_html()
        return html

    def save_html(self, content):
        with open('html.cache', 'w') as f:
            f.write(content)

    def load_html(self):
        with open('html.cache', 'r') as f:
            return f.read()

    def request_html(self, url):
        r = requests.get(self.url)
        html_page = r.content
        return html_page

class ParserClubeFiiTable:
    def __init__(self, html):
        self.table = self._get_table(html)

    def _get_table(self, html_content):
        tree = html.fromstring(html_content)
        table = tree.xpath('//table[@id="table_data_fis"]')
        table = table[0]
        return table

    def parse_table(self):
        for elem in self.table:
            if 'tr' == elem.tag:
                yield elem


    def parse_row(self, row):
        if 'tr' == row.tag:
            elements = row.xpath('.//td')
            return [self._extract_info(elem) for elem in elements]
        return []

    def _extract_info(self, elem):
        text = elem.text
        if None == text:
            children = elem.xpath('.//a')
            for child in children:
                print(child.getchildren())
            elements = [child.text for child in children]
            text = elements[0]
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

    def finaldiscountrate(self, rate, rf, risk_rate):
        return rate * (1-rf) * (1+risk_rate)

    def monthlydiscounterate(self, final_discount_rate):
        # http://fazaconta.com/taxa-mensal-vs-anual.htm
        return ((1+final_discount_rate) ** 1/12) - 1

    def fairprice(self, final_discount_rate):
        price = self.yield12 / self.monthlydiscounterate(final_discount_rate)
        return (price, price/self.price)

    def __str__(self):
        final_discount_rate = self.finaldiscountrate(0.1248, 0.175, 0.10)
        return "{}\tR$ {}\t{}\t{}\t{}\t{} {}".format(\
            self.code, \
            self.price, \
            self.yield1, \
            self.monthlydiscounterate(final_discount_rate), \
            self.yield12, \
            final_discount_rate, \
            self.fairprice(final_discount_rate)
        )

if __name__ == '__main__':
    crawler = CrawlerClubeFii()
    content = crawler.load_fiis()

    parser = ParserClubeFiiTable(content)
    for row in parser.parse_table():
        parsed_row = parser.parse_row(row)
        print(parsed_row)

    #for row in table:
    #    print(row)
        #fii = Fii(crawler.parserow(row))
        #print("{}".format(fii))
