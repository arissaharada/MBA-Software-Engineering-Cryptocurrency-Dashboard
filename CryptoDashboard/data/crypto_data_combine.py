import pandas as pd

# Carregando os dois arquivos de dados novos
data1 = pd.read_csv(r"C:\Users\Arissa\Desktop\CryptoDashboard\raw\crypto_data_combined1.csv")
data2 = pd.read_csv(r"C:\Users\Arissa\Desktop\CryptoDashboard\raw\crypto_data_combined2.csv")

# Combinando os dados
combined_data = pd.concat([data1, data2], ignore_index=True)

# Convertendo a coluna de datas para formato datetime
combined_data['date'] = pd.to_datetime(combined_data['date'])

# Verificando se o arquivo combinado já existe
try:
    # Carregando o arquivo CSV existente, se já houver um
    existing_data = pd.read_csv("combined_crypto_data.csv")
    
    # Convertendo as datas do arquivo existente
    existing_data['date'] = pd.to_datetime(existing_data['date'])
    
    # Concatenando os dados novos aos já existentes
    combined_data = pd.concat([existing_data, combined_data], ignore_index=True)
    
    # Removendo duplicatas (caso existam registros com a mesma data e criptomoeda)
    combined_data = combined_data.drop_duplicates(subset=['crypto', 'date'], keep='last')
    
except FileNotFoundError:
    # Caso o arquivo não exista, os dados novos serão os únicos
    print("Arquivo combinado não encontrado. Criando novo arquivo com os dados.")

# Salvando o arquivo combinado sem substituir os dados antigos, apenas adicionando novos
combined_data.to_csv("combined_crypto_data.csv", index=False)
