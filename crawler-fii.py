import requests
import time
import argparse
from os import path,stat
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from lxml import html

def load_fiis():
    filename = 'html.cache'
    html = ''
    if path.isfile(filename):
        # time since last modification in minutes should be less than 1 hour
        if (time.time() - stat(filename).st_mtime) / 60 > 60:
            html = request_html()
            save_html(html)
        else:
            html = load_html()
    else:
        html = request_html()
        save_html(html)
    return html

def fake_load_fiis():
    html = load_html()
    return html

def request_html():
    url = 'https://www.clubefii.com.br/proventos-rendimento-distribuicoes-amortizacoes'

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    # driver.implicity_wait(30)
    driver.get(url)

    table = driver.find_element_by_xpath("//table")
    tableHTML = table.get_attribute("innerHTML")
    driver.quit()

    return tableHTML


def save_html(content):
    with open('html.cache', 'w') as f:
        f.write(content)

def load_html():
    with open('html.cache', 'r') as f:
        return f.read()

class Fii:

    def __init__(self, raw):
        tr = raw
        children = tr.getchildren()

        self.code = children[0].getchildren()[0].text
        #self.name = children[1].getchildren()[0].text
        try:
            self.total = children[2].getchildren()[0].getchildren()[0].text
            self.total = self._format_price(self.total)
        except:
            self.total = None
        self.price = self._format_price(children[3].getchildren()[0].text)
        self.yield1 = self._format_yield(children[4].getchildren()[0].text)
        self.yield12 = self._format_yield(children[5].getchildren()[0].text)
        self.type = children[6].getchildren()[0].text
        self.ref = children[7].getchildren()[0].text
        self.base = children[8].getchildren()[0].text
        self.payment = children[9].getchildren()[0].text


    def _format_price(self, text):
        try:
            text = text.replace('R$','').replace('.','').replace(',','.')
            return float(text)
        except:
            return None

    def _format_yield(self, text):
        try:
            text = text.replace('%','').replace(',','.')
            return float(text)
        except:
            return None

    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(\
        self.code, \
        self.total,\
        self.price,\
        self.yield1,\
        self.yield12,\
        self.ref,\
        self.base,\
        self.payment\
        )

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bech', type=float)
    parser.add_argument('--rf', type=float)
    parser.add_argument('--risk',type=float)

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    tableHTML = load_fiis()
    table_tree = html.fromstring(tableHTML)
    table_id = "table_data_fis"
    rows = table_tree.xpath("//tbody/tr")

    for row in rows:
        if 'tr' == row.tag:
            fii = Fii(row)
            print(fii)
