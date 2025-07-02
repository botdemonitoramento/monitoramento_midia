from newspaper import Article
from newspaper import Config
import pandas as pd
import time
import feedparser
import pandas as pd
import google.generativeai as genai
import time
import os

def extrair_url_real(google_rss_url):
    from urllib.parse import urlparse, parse_qs
    
    # Faz o parse da URL
    parsed_url = urlparse(google_rss_url)
    
    # Extrai os parâmetros da query
    params = parse_qs(parsed_url.query)
    
    # Pega o valor do parâmetro 'url'
    url_real = params.get('url', [None])[0]
    
    return url_real


rss_link = {'xp': ['https://www.google.com.br/alerts/feeds/09404460482838700245/5822277793724032524']}

list = []
for gestora, urls in rss_link.items():
    for i in range(len(urls)):

        feed = feedparser.parse(urls[i])

        for entry in feed.entries:
            dict = {}
            dict['gestora'] = gestora
            dict['titulo'] = entry.title
            dict['link'] = entry.link
            dict['date'] = entry.published
            list.append(dict)


news_df = pd.DataFrame(list)
news_df['link_limpo'] = news_df['link'].apply(extrair_url_real)
news_df = news_df.drop_duplicates('link_limpo')



genai.configure(api_key="AIzaSyAodyBl0O3ufE0x1-9nubUljeu6sOKQfjk")


# Configuração
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

# Inicializa o modelo
model = genai.GenerativeModel("gemini-2.0-flash")

# Lista para armazenar resultados
results = []

# Loop pelas notícias
for ind in news_df.index:
    url = news_df['link_limpo'][ind]
    date = news_df['date'][ind]
    gestora = news_df['gestora'][ind]
    titulo = news_df['titulo'][ind]

    try:
        article = Article(url, config=config)
        article.download()
        article.parse()

        prompt_analista = f""" Você é um analista de notícias financeiras experiente e conciso. Sua tarefa é extrair informações cruciais.
        Faça um breve resumo do seguinte artigo:

        {article.text}
        """

        response_1 = model.generate_content(prompt_analista)

        

        # Espera para respeitar o limite de requisições
        time.sleep(4)

        prompt_compliance = f""""Você é um especialista em compliance e riscos legais. A gestora {gestora} presta serviço a empresa que você atua, a diretoria confiou a tarefa de ler e avaliar
          a seguinte notícia e inofrmar se a {gestora} representa um risco legal ou a imagem da empresa, se a {gestora} representar um risco retorne apenas a palavra sim, se existe a possibilidade
            de representar um risco retorne a palavra possivel e se {gestora} não representar nenhum risco retorne a palavra nao. Segue o artigo:
        {article.text}
        """

        response_2 = model.generate_content(prompt_compliance)
        
        results.append({
            'gestora': gestora,
            'url': url,
            'date': date,
            'title': article.title,
            'resumo': response_1.text.strip(),
            'risco':response_2.text.strip()
        })
        time.sleep(4)

    except Exception as e:
        print(f"Erro ao processar URL: {url}\nMotivo: {e}\n")

        # Verifica se o erro é de limite de requisições
        if "429" in str(e):
            print("Limite de requisições excedido. Aguardando 60 segundos...\n")
            time.sleep(60)

        results.append({
            'gestora': gestora,
            'url': url,
            'date': date,
            'title': titulo,
            'resumo': 'sem_resumo',
            'risco': 'sem_info'
        })

        continue  # Pula para o próximo artigo

# Cria DataFrame final
news = pd.DataFrame(results)

news

news_risco = news[news.risco == 'sim' | news.risco == 'possivel']

