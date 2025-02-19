import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_resposta_da_url(url: str)-> object | None:
    """Realiza uma requisição GET para a URL fornecida e retorna a resposta."""
    response = requests.get(url)
    if response.status_code == 200:
        print('Requisição bem sucedida !')
        return response
    print('Problema na requisição !')
    return None

def extrair_dados_da_tabela(soup):
    """Extrai os dados da tabela HTML usando BeautifulSoup."""
    table = soup.find('table', {'id': 'grd_DXMainTable'})
    rows = table.find_all('tr')

    data_list = []
    price_list = []

    for row in rows:
        columns = row.find_all('td', {'class': 'dxgv'})
        if len(columns) == 2:
            data = columns[0].text.strip()
            price = columns[1].text.strip()
            data_list.append(data)
            price_list.append(price)

    return data_list, price_list

def criar_dataframe(data_list, price_list):
    """Cria e retorna um DataFrame com os dados extraídos."""
    df = pd.DataFrame({
                        'Data': data_list,
                        'Preço_Brent': price_list
                    })
    return df

def web_scraping_dados_ipea():
    """Função principal que executa o processo completo."""
    url = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
    
    response = obter_resposta_da_url(url)
    
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        data_list, price_list = extrair_dados_da_tabela(soup)

        df = criar_dataframe(data_list, price_list)
        return df 

if __name__ == '__main__':
    web_scraping_dados_ipea()
