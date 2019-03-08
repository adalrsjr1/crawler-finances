import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html

def print_node(node):
    print(node)
    for child in node:
        print(child)
        print_node(child)

if __name__ == "__main__":
    url = 'https://www.clubefii.com.br/proventos-rendimento-distribuicoes-amortizacoes'

    driver = webdriver.Firefox()
    driver.implicity_wait(30)
    driver.get(url)

    table = driver.find_element_by_id('table_data_fis')
    print(table)

    # tree = html.fromstring(r.content)
    # table_id = "table_data_fis"
    # node = tree.xpath("//div[@id='div_id_central_tabela']")

    # print_node(node)
