from pygooglenews import GoogleNews
import pandas as pd
import numpy as np
from textblob import TextBlob

def get_titles(keywords):
    """
    Busca notícias no Google News para as palavras-chave fornecidas.
    """
    gn = GoogleNews(lang='en')  # Notícias em inglês
    all_news = []
    
    for keyword in keywords:
        print(f"Buscando notícias para a palavra-chave: {keyword}...")
        search = gn.search(keyword)  # Busca notícias para cada palavra-chave
        if search and 'entries' in search:
            articles = search['entries']
            for i in articles:
                article = {
                    'title': i.get('title', 'No Title'),
                    'link': i.get('link', 'No Link'),
                    'published': i.get('published', 'No Date'),
                    'keyword': keyword  # Para identificar a palavra-chave associada
                }
                all_news.append(article)
        else:
            print(f"⚠️ Nenhum artigo encontrado para: {keyword}")
    
    return all_news

# Palavras-chave para busca
keywords = ['Cryptocurrency', 'Bitcoin', 'Blockchain', 'Crypto market', 'Trump', 'Dogecoin', 'Elon Musk', 'Crypto', 'Ethereum', 'Solana', 'RNDR', 'Cardano', 'Chainlink', 'Uniswap', 'Render Token', 'Axie Infinity']

# Busca notícias
data = get_titles(keywords)

# Verifica os resultados
if data:
    print(f"{len(data)} artigos encontrados!")
else:
    print("Nenhuma notícia foi encontrada.")

# Criação do DataFrame
df = pd.DataFrame(data)

# Análise de sentimento
def sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

df['sentiment'] = df['title'].apply(sentiment)
df['Sentiment Class'] = np.where(df['sentiment'] < 0, 'negative',
                                 np.where(df['sentiment'] > 0, 'positive', 'neutral'))

# Tratamento da data
df['Date'] = pd.to_datetime(df['published'], errors='coerce')  # Ignora erros na conversão
df['Date'] = df['Date'].dt.date
df = df.sort_values(by='Date', ascending=False)

# Exportação para CSV
output_file = 'crypto_news.csv'
df.to_csv(output_file, index=False)
print(f"✅ Arquivo salvo como: {output_file}")

# Estatísticas básicas de sentimento
print("Análise de sentimentos:")
print(df['Sentiment Class'].value_counts(normalize=True))
