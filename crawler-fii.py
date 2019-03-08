import requests
import time
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

def print_node(node):
    print(node)
    for child in node:
        print(child)
        print_node(child)

class Fii:
    def __init__(self, raw):
        pass

    def __str__(self):
        pass

if __name__ == "__main__":
    tableHTML = load_fiis()
    table_tree = html.fromstring(tableHTML)
    table_id = "table_data_fis"
    rows = table_tree.xpath("//tbody/tr")

    for row in rows:
        print_node(row)
