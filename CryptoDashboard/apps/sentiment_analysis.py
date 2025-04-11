import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px
from app import app

# Carregar os dados das notícias
news_data = pd.read_csv("crypto_news.csv")
news_data['Date'] = pd.to_datetime(news_data['Date'])

# Carregar os dados das criptomoedas
crypto_data = pd.read_csv("combined_crypto_data.csv")
crypto_data['date'] = pd.to_datetime(crypto_data['date'])

# Função para traduzir meses para português e abreviar
def traduzir_meses(date_series):
    meses_pt = {
        "January": "Jan", "February": "Fev", "March": "Mar",
        "April": "Abr", "May": "Mai", "June": "Jun",
        "July": "Jul", "August": "Ago", "September": "Set",
        "October": "Out", "November": "Nov", "December": "Dez"
    }
    # Converte a série para datetime, se ainda não for
    date_series = pd.to_datetime(date_series)
    # Formata o mês e o ano em português (abreviado)
    return date_series.dt.strftime('%Y-%m').apply(lambda x: f"{meses_pt[pd.to_datetime(x).strftime('%B')]} {pd.to_datetime(x).strftime('%Y')}")

# Função para traduzir as classes de sentimentos
def traduzir_sentimentos(sentiment_class):
    sentimentos_pt = {
        "positive": "Positivo",
        "negative": "Negativo",
        "neutral": "Neutro"
    }
    return sentimentos_pt.get(sentiment_class, sentiment_class)  # Retorna o valor traduzido ou o original se não houver tradução

# Função para filtrar os dados das notícias
def filter_news_by_date(start_date, end_date):
    if start_date and end_date:
        return news_data[(news_data['Date'] >= start_date) & (news_data['Date'] <= end_date)]
    return news_data

# Função para filtrar os dados das criptomoedas
def filter_crypto_data(crypto, start_date, end_date):
    filtered_data = crypto_data[crypto_data['crypto'] == crypto]
    if start_date and end_date:
        return filtered_data[(filtered_data['date'] >= start_date) & (filtered_data['date'] <= end_date)]
    return filtered_data

# Layout do dashboard
layout = html.Div([
    # Linha 1: Filtros e gráfico combinado
    html.Div([
        # Coluna 1: Filtros
        html.Div([
            html.H2("Filtros:", className="dash-title"),
            html.Label("Selecione o período:", className='mb-2'),
            dcc.DatePickerRange(
                id="date-picker-range",
                start_date="2024-01-01",
                end_date="2025-01-01",
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '15px', 'width': '100%'}
            ),
            html.Label("Selecione a moeda:", className='mb-2'),
            dcc.Dropdown(
                id="crypto-selector",
                options=[
                    {"label": crypto, "value": crypto} for crypto in crypto_data['crypto'].unique()
                ],
                value=crypto_data['crypto'].unique()[0],
                multi=False,
                style={'margin-bottom': '15px'}
            ),
        ], className='filter-container'),
        
        # Coluna 2: Gráfico combinado (sentimento e preço/volume)
        html.Div([
            dcc.Graph(id='combined-graph', style={'height': '400px'}),
        ], className='chart-container')
    ], className='row-container'),

    # Linha 2: Tabela de resumo e tabela de notícias
    html.Div([
        # Coluna 1: Tabela de resumo dos sentimentos
        html.Div([
            html.H2("Resumo dos Sentimentos", className="dash-title"),
            dash_table.DataTable(
                id='sentiment-table',
                columns=[
                    {'name': 'Classe de sentimento', 'id': 'Sentiment Class'},
                    {'name': 'Contagem total', 'id': 'Count'}
                ],
                style_table={'margin': '0 auto', 'width': '100%'},
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#111828',
                    'color': '#FFFFFF',
                    'textAlign': 'center',
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#1c2331',
                    'color': '#FFFFFF',
                    'fontFamily': 'Arial, sans-serif',
                },
            )
        ], className='table-container'),
        
        # Coluna 2: Tabela de notícias
        html.Div([
            html.H2("Notícias no Período Selecionado", className="dash-title"),
            dash_table.DataTable(
                id='news-table',
                columns=[
                    {'name': 'Título', 'id': 'title', 'deletable': False},
                    {'name': 'Data', 'id': 'Date', 'deletable': False},
                    {'name': 'Sentimento', 'id': 'sentiment', 'deletable': False}
                ],
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#111828',
                    'color': '#FFFFFF',
                    'textAlign': 'center',
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#1c2331',
                    'color': '#FFFFFF',
                    'fontFamily': 'Arial, sans-serif',
                    'white-space': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                page_size=10,
                style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
            )
        ], className='table-container', style={'padding-top': '20px'})
    ], className='row-container')
], className='content-container', style={'padding': '20px 0'})

# Callbacks para atualizar os gráficos e a tabela
@callback(
    [
        Output('combined-graph', 'figure'),
        Output('sentiment-table', 'data'),
        Output('news-table', 'data')
    ],
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('crypto-selector', 'value')
    ]
)
def update_content(start_date, end_date, selected_crypto):
    # Filtrar os dados das notícias e das criptomoedas
    filtered_news = filter_news_by_date(start_date, end_date)
    filtered_crypto = filter_crypto_data(selected_crypto, start_date, end_date)

    # Adicionar a classe de sentimento (Sentiment Class) aos dados de notícias
    news_summary = filtered_news.groupby('Date').agg(
        sentiment=('sentiment', 'mean'),
        sentiment_class=('Sentiment Class', lambda x: ', '.join(set(x)))
    ).reset_index()

    # Traduzir os sentimentos para português
    news_summary['sentiment_class'] = news_summary['sentiment_class'].apply(
        lambda x: ', '.join([traduzir_sentimentos(s.strip()) for s in x.split(',')])
    )

    # Combinar dados de sentimento e de criptomoeda
    combined_data = pd.merge(
        news_summary,
        filtered_crypto[['date', 'close', 'volume']],
        left_on='Date', right_on='date',
        how='inner'
    )

    # Criar rótulos para o eixo x (6 meses distribuídos uniformemente)
    date_range = pd.date_range(start=combined_data['Date'].min(), end=combined_data['Date'].max(), periods=6)
    tickvals = date_range
    ticktext = [traduzir_meses(pd.Series([date]))[0] for date in date_range]

    # Gráfico combinado de sentimento médio e preço
    combined_fig = px.line(
        combined_data, x='Date',
        y=['sentiment', 'close'],
        title=f'Tendência de Sentimento e Preço para {selected_crypto}',
        labels={
            'value': 'Valor',
            'variable': 'Métrica',
            'Date': 'Data',
            'sentiment': 'Sentimento',  # Tradução de "sentiment" para "Sentimento"
            'close': 'Fechamento'      # Tradução de "close" para "Fechamento"
        },
        template="plotly_dark",
        custom_data=['sentiment_class']
    )

    # Alterar os nomes das variáveis na legenda
    combined_fig.update_traces(
        name="Sentimento", selector=dict(name="sentiment")
    )
    combined_fig.update_traces(
        name="Fechamento em dólares", selector=dict(name="close")
    )

    # Ajustar o hover
    combined_fig.update_traces(
        hovertemplate=(
            'Data: %{x}<br>' +
            'Métrica: %{fullData.name}<br>' +
            'Valor: %{y}<br>' +
            'Sentimento: %{customdata[0]}<extra></extra>'
        )
    )

    # Ajustar eixos
    combined_fig.update_xaxes(
        tickvals=tickvals,  # Valores dos ticks
        ticktext=ticktext,  # Rótulos dos ticks
        tickangle=0  # Rótulos horizontais
    )

    # Atualizar tabela de resumo
    sentiment_summary = filtered_news['Sentiment Class'].value_counts().reset_index()
    sentiment_summary.columns = ['Sentiment Class', 'Count']
    sentiment_summary['Sentiment Class'] = sentiment_summary['Sentiment Class'].apply(traduzir_sentimentos)  # Traduzir sentimentos

    # Atualizar tabela de notícias
    news_table_data = filtered_news[['title', 'Date', 'sentiment']].to_dict('records')

    return combined_fig, sentiment_summary.to_dict('records'), news_table_data