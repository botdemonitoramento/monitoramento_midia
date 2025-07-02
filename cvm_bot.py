#Bibliotecas

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import smtplib
from email.message import EmailMessage

#Função que encontra e retorna informações sobre a palavra chave.
def LocalizaNews(palavra_chave):
    service = Service()
    options = webdriver.ChromeOptions()
    # Modo headless (não abre o navegador na tela)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # ajuda no Windows
    
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.gov.br/cvm/pt-br/search?origem=form&SearchableText="+palavra_chave

    driver.get(url)
    # Cria o objeto de espera
    wait = WebDriverWait(driver, 10)

    # Espera até que o botão esteja clicável
    botao_rejeitar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'reject-all') and @aria-label='Rejeitar cookies']")))
    botao_rejeitar.click()


    noticias_links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    datas = driver.find_elements(By.CLASS_NAME, "data")

    titulo = noticias_links[274].text
    link = noticias_links[274].get_attribute("href")
    data_str = datas[0].text.replace('-','').strip()
    data = datetime.strptime(data_str, '%d/%m/%Y')



    df = {"Título": titulo,
        'Link': link,
        'Data': data.strftime('%d/%m/%Y')}
    
    

    return df

#teste
palavra_de_busca = ['Tivio', 'xp', 'vinci', 'tarpon', 'bnp', 'oceana']
texto = LocalizaNews(palavra_de_busca[1])

print(texto)
