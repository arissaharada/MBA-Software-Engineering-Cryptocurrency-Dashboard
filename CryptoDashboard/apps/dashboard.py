import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

# Importar pacotes necessários
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from apps.narrativas import narrativas  # Importar narrativas

# Carregar os dados
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "combined_crypto_data.csv"))
data = pd.read_csv(csv_path)
data['date'] = pd.to_datetime(data['date'])

# Adicionar narrativa principal e relacionadas
data['narrativa_principal'] = data['crypto'].map(lambda x: narrativas.get(x, {}).get("principal", "Não disponível"))
data['narrativa_relacionada'] = data['crypto'].map(lambda x: narrativas.get(x, {}).get("relacionadas", []))

# Função para converter meses para português e abreviar
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

# Função para criar a seção de narrativas
def create_narratives_section(selected_crypto, narrativa_principal_text, narrativa_relacionada_text):
    return html.Div(
        [
            html.H2("Moeda:", className="dash-title"),
            html.Div(id="narrativa_principal", className='p-3 mb-4', children=narrativa_principal_text),
            html.H4("Narrativas Relacionadas:", className='mb-3'),
            html.Div(id="narrativa_relacionada", className='p-3', children=narrativa_relacionada_text)
        ],
        className='narratives-container'
    )

# Função para gerar o conteúdo das narrativas
def generate_narrative_content(narrativa, selected_crypto):
    # Narrativa Principal
    principal = narrativa.get("principal", "Não disponível")
    explicacao_principal = narrativa.get("explicacao", "Sem explicação disponível.")
    
    narrativa_principal_text = html.Div([
        html.H3(f"{selected_crypto}"),
        html.P(f"{explicacao_principal}"),
        html.H4("Narrativa Principal:"),
        html.P(f"{principal}")
    ])

    # Narrativas Relacionadas
    relacionadas = narrativa.get("relacionadas", [])
    relacionadas_explicacoes = narrativa.get("relacionadas_explicacoes", {})
    
    narrativa_relacionada_text = html.Ul([
        html.Li(f"{relacionada}: {relacionadas_explicacoes.get(relacionada, 'Sem explicação disponível.')}")
        for relacionada in relacionadas
    ]) if relacionadas else "Não disponível"

    return narrativa_principal_text, narrativa_relacionada_text

# Layout do Dashboard
layout = html.Div([
    # Linha 1: Filtros, gráfico de preços e narrativas
    html.Div(
        [
            # Coluna 1: Filtros
            html.Div(
                [
                    html.H2("Filtros:", className="dash-title"),
                    html.Label("Selecione o período:", className='mb-2'),
                    dcc.DatePickerRange(
                        id="date_picker",
                        start_date="2024-01-01",
                        end_date="2025-01-01",
                        display_format="YYYY-MM-DD",
                        style={'margin-bottom': '15px', 'width': '100%'}
                    ),
                    html.Label("Selecione a moeda:", className='mb-2'),
                    dcc.Dropdown(
                        id="crypto_selector",
                        options=[{"label": crypto, "value": crypto} for crypto in data['crypto'].unique()],
                        multi=False,
                        style={'margin-bottom': '15px'}
                    ),

                    html.Label("Escolha os preços para exibição:", className='mb-2'),
                    dcc.Checklist(
                        id="price_type_selector",
                        options=[
                            {"label": "Abertura (Open)", "value": "open"},
                            {"label": "Alta (High)", "value": "high"},
                            {"label": "Baixa (Low)", "value": "low"},
                            {"label": "Fechamento (Close)", "value": "close"}
                        ],
                        value=["open", "high", "low", "close"],
                        inline=False,
                        style={'margin-bottom': '15px'}
                    )
                ],
                className='filter-container'
            ),

            # Coluna 2: Gráfico de preços
            html.Div(
                [
                    dcc.Graph(id="price_chart", style={'height': '400px'})
                ],
                className='chart-container'
            ),

            # Coluna 3: Narrativas
            create_narratives_section(None, None, None)
        ],
        className='row-container'
    ),

    # Linha 2: Gráfico de volume e estatísticas
    html.Div(
        [
            # Coluna 1: Gráfico de volume
            html.Div(
                [
                    dcc.Graph(id="volume_chart", style={'height': '400px'})
                ],
                className='volume-container'
            ),

            # Coluna 3: Estatísticas de volume e gráfico relacionado
            html.Div(
                [
                    html.Div(
                        [
                            html.H2("Estatísticas por Mês/Ano:", className="dash-title"),
                            html.Table(
                                id="volume_stats_table",
                                className='styled-table',
                                style={"width":"100%", "height": "300px", "overflowY": "scroll", "display": "block"}
                            )
                        ],
                        style={'width': '40%', 'padding': '10px'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="stats_related_chart", style={'height': '400px', 'width': '100%'})
                        ],
                        style={'width': '60%', 'padding': '10px'}
                    )
                ],
                className='stats-container',
                style={'display': 'flex', 'justify-content': 'space-between'}
            )
        ],
        className='row-container'
    )
])      

# Atualização dos gráficos e estatísticas
@app.callback(
    [
        Output("price_chart", "figure"),
        Output("volume_chart", "figure"),
        Output("narrativa_principal", "children"),
        Output("narrativa_relacionada", "children"),
        Output("volume_stats_table", "children"),
        Output("stats_related_chart", "figure")
    ],
    [
        Input("crypto_selector", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
        Input("price_type_selector", "value")
    ]
)
def update_dashboard(selected_crypto, start_date, end_date, selected_prices):
    # Filtrar dados
    filtered_data = data[
        (data['crypto'] == selected_crypto) &
        (data['date'] >= start_date) &
        (data['date'] <= end_date)
    ]

    # Verificar se há dados filtrados
    if filtered_data.empty:
        # Retornar gráficos e tabelas vazios ou com mensagem de erro
        empty_fig = px.line(title="Nenhum dado disponível para o período selecionado")
        empty_fig.update_layout(template="plotly_dark")
        empty_table = [html.Tr([html.Td("Nenhum dado disponível", colSpan=4)])]
        return empty_fig, empty_fig, "Nenhuma narrativa disponível", "Nenhuma narrativa relacionada", empty_table, empty_fig

    # Criar rótulos para o eixo x (6 meses distribuídos uniformemente)
    date_range = pd.date_range(start=filtered_data['date'].min(), end=filtered_data['date'].max(), periods=6)
    tickvals = date_range
    ticktext = [traduzir_meses(pd.Series([date]))[0] for date in date_range]

    # Gráfico de preços
    price_fig = px.line(
        filtered_data,
        x="date",
        y=selected_prices,
        title=f"Preços de {selected_crypto}",
        template="plotly_dark",
        labels={"value": "Valor em dólares", "date": "Data"}
    )

    # Alterar os nomes das variáveis na legenda
    price_fig.update_traces(
        name="Abertura", selector=dict(name="open")
    )
    price_fig.update_traces(
        name="Alta", selector=dict(name="high")
    )
    price_fig.update_traces(
        name="Baixa", selector=dict(name="low")
    )
    price_fig.update_traces(
        name="Fechamento", selector=dict(name="close")
    )

    # Alterar o título da legenda
    price_fig.update_layout(legend_title_text="Variáveis")

    # Ajustar eixos
    price_fig.update_xaxes(
        tickvals=tickvals,  # Valores dos ticks
        ticktext=ticktext,  # Rótulos dos ticks
        tickangle=0  # Rótulos horizontais
    )

    # Gráfico de volume
    volume_fig = px.bar(
        filtered_data,
        x="date",
        y="volume",
        title=f"Volume Negociado de {selected_crypto}",
        template="plotly_dark",
        labels={"volume": "Volume", "date": "Data"}
    )
    volume_fig.update_xaxes(
        tickvals=tickvals,  # Valores dos ticks
        ticktext=ticktext,  # Rótulos dos ticks
        tickangle=0  # Rótulos horizontais
    )

    # Narrativas
    narrativa = narrativas.get(selected_crypto, {})
    narrativa_principal_text, narrativa_relacionada_text = generate_narrative_content(narrativa, selected_crypto)

    # Agrupar por Mês/Ano
    filtered_data['month_year'] = filtered_data['date'].dt.to_period('M')
    monthly_stats = filtered_data.groupby('month_year')['volume'].agg(['mean', 'max', 'min']).reset_index()
    monthly_stats['month_year'] = traduzir_meses(monthly_stats['month_year'].astype(str))

    # Tabela de estatísticas por mês/ano
    volume_stats_table = [
        html.Thead(html.Tr([
            html.Th("Mês/Ano", style={"background-color": "#111828", "color": "#ffffff", "text-align": "center"}),
            html.Th("Média", style={"background-color": "#111828", "color": "#ffffff", "text-align": "center"}),
            html.Th("Máximo", style={"background-color": "#111828", "color": "#ffffff", "text-align": "center"}),
            html.Th("Mínimo", style={"background-color": "#111828", "color": "#ffffff", "text-align": "center"})
        ])),
        html.Tbody([
            html.Tr([
                html.Td(row['month_year']),
                html.Td(f"{row['mean']:.2f}"),
                html.Td(f"{row['max']:.2f}"),
                html.Td(f"{row['min']:.2f}")
            ]) for _, row in monthly_stats.iterrows()
        ])
    ]

    # Gráfico de linhas comparativas
    stats_related_chart = px.line(
        monthly_stats,
        x="month_year",
        y=["mean", "max", "min"],
        labels={"value": "Volume", "month_year": "Mês/Ano", "variable": "Estatística"},
        title="Estatísticas Mensais de Volume",
        template="plotly_dark"
    )

    # Alterar os nomes das variáveis na legenda
    stats_related_chart.update_traces(
        name="Média", selector=dict(name="mean")
    )
    stats_related_chart.update_traces(
        name="Máximo", selector=dict(name="max")
    )
    stats_related_chart.update_traces(
        name="Mínimo", selector=dict(name="min")
    )

    # Alterar o título da legenda
    stats_related_chart.update_layout(legend_title_text="Estatística")

    return price_fig, volume_fig, narrativa_principal_text, narrativa_relacionada_text, volume_stats_table, stats_related_chart

if __name__ == '__main__':
    app.run_server(debug=True)