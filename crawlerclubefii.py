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
                html = self.request_html(self.url)
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
            return [self._format_info(self._extract_info(elem)) for elem in elements[:7]]
        return []

    def _extract_info(self, elem):
        info = None
        if 'td' != elem.tag:
            return None

        info = elem.xpath('.//a')[0]
        children = info.getchildren()

        if 0 == len(children):
            return info.text
        else:
            return children[0].text

    def _format_info(self, elem):
        elem = elem.replace('\\r\\n','').strip()

        if 'N/D' == elem:
            return -1.0

        try:
            return float(elem.replace('R$','').replace('%','').replace('.','').replace(',','.'))
        except:
            return elem

class Fii:
    def __init__(self, discount_rate, rf, risk_rate, values):
        self.discount_rate = discount_rate
        self.rf = rf
        self.risk_rate = risk_rate
        self.code = values[0]
        self.name = values[1]
        self.price = values[2]
        self.equity_price = values[3]
        self.yield1 = values[4]/100
        self.yield12 = values[5]/100
        self.type = values[6][0]

    def __str__(self):
        color = '\033[92m' # green
        endcolor = '\033[0m'
        if self.downside():
            color = '\33[91m'

        return '{}{:>10} R$ {:<10.2f} R$ {:<10.2f} R$ {:<10.2f} {:5.2f}% {:10.4f} {} {}'.format(\
        color,\
        self.code, \
        self.price,\
        self.fair_price(),
        self.equity_price,\
        self.average_yield()*100,\
        self.downside_value(),\
        'D' if self.downside() else 'U',\
        endcolor,\
        )

    def  equity_price(self):
        return self.equity * self.price

    def yield1_price(self):
        return self.yield1 * self.price

    def yield12_price(self):
        return self.yield12 * self.price

    def final_discount_rate(self):
        return self.discount_rate * (1-self.rf) * (1+self.risk_rate)

    def monthly_discounte_rate(self):
        # http://fazaconta.com/taxa-mensal-vs-anual.htm
        return ((1+self.final_discount_rate()) ** (1/12))-1

    def downside(self):
        return self.yield1 < self.monthly_discounte_rate()

    def downside_value(self):
        return self.fair_price_perc() - 1

    def average_yield(self):
        return ((self.yield12 + 1) ** (1/12)) - 1

    def fair_price(self):
        price = (self.yield1_price() / self.monthly_discounte_rate())
        return price 

    def fair_price_perc(self):
        return self.fair_price()/self.price

if __name__ == '__main__':
    #print(Fii(12.48/100, 0.1750, 0.10, ['XXXX', '', 100.00, 0, 0.83, 0.1047, 'a']))

    crawler = CrawlerClubeFii()
    content = crawler.load_fiis()

    parser = ParserClubeFiiTable(content)

    for row in parser.parse_table():
        parsed_row = parser.parse_row(row)
        fii = Fii(6.4492/100, 0.175, 0.20, parsed_row)
        print(fii)
