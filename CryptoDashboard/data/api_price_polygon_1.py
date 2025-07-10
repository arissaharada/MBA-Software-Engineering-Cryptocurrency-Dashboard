import requests
import pandas as pd
from datetime import datetime, timezone
import os

# Configuração do caminho de salvamento
caminho_pasta = os.path.expanduser("~/Desktop/CryptoDashboard/raw/")
os.makedirs(caminho_pasta, exist_ok=True)  # cria a pasta se não existir

# Chave da API
API_KEY = 'YOUR_API'  # Substitua pela sua chave da API

# Período desejado
START_DATE = "2022-07-01"  # Data de início
END_DATE = datetime.today().strftime('%Y-%m-%d')    # Data de término - define o END_DATE como a data de hoje no formato YYYY-MM-DD como exigido pela API

# Dicionário com os tickers das criptomoedas
CRYPTO_TICKERS = {
    "X:BTCUSD": "Bitcoin",
    "X:ETHUSD": "Ethereum",
    "X:SOLUSD": "Solana",
    "X:ADAUSD": "Cardano",
    "X:LINKUSD": "Chainlink"
}

# Função para coletar dados de uma criptomoeda
def get_crypto_data(api_key, crypto_pair, start_date, end_date, crypto_name):
    base_url = f"https://api.polygon.io/v2/aggs/ticker/{crypto_pair}/range/1/day/{start_date}/{end_date}"
    all_data = []

    params = {
        'adjusted': 'true',
        'sort': 'asc',
        'apiKey': api_key,
        'limit': 50000
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'results' in data:
            for item in data['results']:
                all_data.append({
                    'crypto': crypto_name,
                    'date': datetime.fromtimestamp(item['t'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d'),
                    'open': item['o'],
                    'high': item['h'],
                    'low': item['l'],
                    'close': item['c'],
                    'volume': item['v']
                })

        if not all_data:
            print(f"Nenhum dado encontrado para o período especificado para {crypto_pair}.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados de preços para {crypto_pair}:", e)

    return all_data

# Função para salvar dados em CSV
def save_combined_crypto_data_to_csv(data, filename):
    if not data:
        print(f"Nenhum dado encontrado para {filename}.")
        return

    file_path = os.path.join(caminho_pasta, filename)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Dados combinados salvos em {file_path}.")

def main():
    combined_data = []

    # Itera sobre o dicionário para coletar dados de todas as criptomoedas
    for ticker, name in CRYPTO_TICKERS.items():
        print(f"Coletando dados de {name} ({ticker})...")
        crypto_data = get_crypto_data(API_KEY, ticker, START_DATE, END_DATE, name)
        combined_data.extend(crypto_data)  # Adiciona os dados coletados à lista principal

    # Salva os dados combinados em um único arquivo CSV
    save_combined_crypto_data_to_csv(combined_data, 'crypto_data_combined1.csv')

if __name__ == "__main__":
    main()
