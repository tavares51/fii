import os
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

import config


def abrir_site(url):
    """
    Função para abrir o browser.
    
    Args:
        url (str): URL do site.
    
    Returns:
        webdriver.Chrome: Instância do navegador Chrome.
    """
    try:
        # Configurar o navegador Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        
        # Inicializar o driver do Chrome
        driver = webdriver.Chrome(options=options)
        
        # Acessar a URL fornecida
        driver.get(url)
        
        # Maximizar a janela do navegador
        driver.maximize_window()
        
        return driver
    except Exception as e:
        # Lidar com exceções ao tentar abrir o site
        raise Exception(f"Erro {str(e)} ao tentar abrir o site: {url}")


def check_popup(driver):
    """
    Verificar e fechar pop-up, se existir.
    
    Args:
        driver (webdriver.Chrome): Instância do navegador Chrome.
    """
    try:
        # Aguardar por 5 segundos para permitir que o pop-up seja exibido
        sleep(5)
        
        # Localizar o elemento do pop-up pelo ID
        dialog = driver.find_element(By.ID, "popup")
        
        # Clicar no botão de fechar do pop-up
        dialog.find_element(By.ID, "popup-close-button").click()
    except Exception:
        # Ignorar exceções se o pop-up não estiver presente
        pass


def extrair_dados(driver):
    """
    Extrair dados da página web e salvar em um arquivo CSV.
    
    Args:
        driver (webdriver.Chrome): Instância do navegador Chrome.
    """
    try:
        # Aguardar por 2 segundos para garantir que a página tenha carregado completamente
        sleep(2)
        
        # Obter o código-fonte HTML da página
        html = driver.page_source.encode('utf-8')
        
        # Criar um objeto BeautifulSoup para análise HTML
        soup = BeautifulSoup(html, 'lxml')
        
        # Lista para armazenar os dados dos fundos imobiliários
        lista_fii = []

        # Extrair nomes das colunas da tabela
        colunas = [coluna.text for coluna in soup.find_all('tr')[0].find_all('th')]

        # Iterar sobre as linhas da tabela e extrair dados
        for row in soup.find_all('tr')[1:]:
            data = row.find_all('td')
            lista_fii.append({
                "Fundos": data[colunas.index('Fundos')].text.strip(),
                "Preço Atual (R$)": data[colunas.index('Preço Atual (R$)')].text.strip(),
                "Liquidez Diária (R$)": data[colunas.index('Liquidez Diária (R$)')].text.strip(),
                "P/VP": data[colunas.index('P/VP')].text.strip(),
                "Último Dividendo": data[colunas.index('Último Dividendo')].text.strip(),
                "Dividend Yield": data[colunas.index('Dividend Yield')].text.strip(),
                "DY (12M) média": data[colunas.index('DY (12M) média')].text.strip(),
                "Variação Preço": data[colunas.index('Variação Preço')].text.strip(),
            })

        # Diretório para salvar relatórios
        reports_dir = config.OUTPUT_DIR
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        # Criar DataFrame do Pandas e salvar em um arquivo CSV
        df_fii = pd.DataFrame(data=lista_fii)
        data_hora_execucao = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        nome_arquivo = f'report_fii_{data_hora_execucao}.csv'
        df_fii.to_csv(os.path.join(reports_dir, nome_arquivo), sep=";")

    except Exception as e:
        # Lidar com exceções ao tentar extrair os dados
        raise Exception(f"Erro {e} ao tentar extrair os Dados.")


def log(message):
    """
    Registrar mensagens de erro em um arquivo de log.
    
    Args:
        message (str): Mensagem de erro.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_erro = f'[{timestamp}] Erro: {message}.'
    
    # Adicionar a mensagem de erro ao arquivo de log
    with open('errors.txt', 'a', encoding='UTF-8') as log_file:
        log_file.write(f'{mensagem_erro}\n')


def run():
    """
    Função principal para executar o script de coleta de dados.
    """
    try:
        # Abrir o site no navegador
        browser = abrir_site(config.URL)
        
        # Verificar e fechar pop-up, se existir
        check_popup(browser)
        
        # Extrair dados da página
        extrair_dados(browser)
        
        print('Processamento finalizado.')

    except Exception as ex:
        # Registrar exceções no arquivo de log
        log(str(ex))


if __name__ == '__main__':
    run()
