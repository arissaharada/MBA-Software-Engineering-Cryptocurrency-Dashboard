# Importar pacotes necessários
import pandas as pd
from dash import dcc, html, dash_table
from app import app

# Carregar os dados
data = pd.read_csv("combined_crypto_data.csv")
data['date'] = pd.to_datetime(data['date'])

# Layout de Dataset
layout = html.Div([
    # Outer Div for content
    html.Div([

        # Descrição do Dataset
        html.Div([
            # html.P("Descrição do Dataset", className='title'),  # Título da seção

            html.Div([
            html.P("Descrição do Dataset:", className='title')
            ]),
            html.Div([  # Texto explicativo
                dcc.Markdown('''
                    Dataset retirado do site Polygon.io para as moedas Bitcoin, Ethereum, Solana, Cardano, Chainlink, Uniswap, Dogecoin, Render Token, Stacks e Axie Infinity
                    no período de 01/11/2022 até 22/01/2025. 
                ''')
            ], className='content-text'),
        ], className='row-container'),

        # Tabela de valores
        html.Div([
            html.Div([
            html.P("Tabela de Valores", className='title')
            ]),
            dash_table.DataTable(
                id='crypto-table',
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict('records'),
                style_table={'height': 'auto', 'overflowX': 'auto', 'width': '100%'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#1c2331',
                    'color': '#ffffff',
                    'fontFamily': 'Arial, sans-serif',
                },
                style_header={
                    'backgroundColor': '#111828',
                    'fontWeight': 'bold',
                    'border': '1px solid #444444',
                },
                style_data={
                    'border': '1px solid #444444',
                },
                fixed_rows={'headers': True},
                page_size=10  # Tamanho da página para exibição inicial
            )
        ], className='row-container')

    ], className='content-container')
])
