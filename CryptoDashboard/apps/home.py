# Importar pacotes necessários
import pandas as pd
from dash import dcc, html
from app import app

# Layout do Home
layout = html.Div([
    html.Div([
        html.Div([
            # Título e texto da seção Objetivo
            html.P("Objetivo", className='title'),
            html.Div([
                dcc.Markdown('''
                    Bem-vindo ao dashboard de criptomoedas.

                    Este dashboard foi desenvolvido para auxiliar pessoas que estão começando a explorar o mundo das criptomoedas e querem entender melhor como esse mercado funciona. 
                    Sabemos que o universo das criptomoedas pode parecer complexo e até intimidador, mas este dashboard foi projetado para simplificar a experiência e tornar o 
                    aprendizado acessível para todos, independentemente do seu nível de conhecimento.

                    O mercado de criptomoedas é conhecido por sua alta volatilidade, influenciado por diversos fatores, como notícias, o sentimento das comunidades, a confiança em
                    determinados projetos e as narrativas que moldam o comportamento dos investidores. 

                    As narrativas têm ganhado foco no estudo do mercado financeiro, sendo os grandes temas ou histórias que guiam o mercado em diferentes momentos. Elas podem tratar de 
                    tópicos como reserva de valor, contratos inteligentes ou até áreas como jogos e tecnologia. Este dashboard permite a identificação das narrativas de dez moedas principais, 
                    correlacionando-as com notícias relevantes e analisando como essas narrativas influenciam o mercado. Também oferecemos análise de preços históricos e volumes de trading, 
                    complementados por análises estatísticas detalhadas para o período selecionado.

                    Além disso, o dashboard inclui uma análise de sentimento baseada em notícias do mercado financeiro, permitindo identificar a quantidade de notícias positivas, negativas 
                    ou neutras sobre criptomoedas no período escolhido. As moedas analisadas neste dashboard são: **Bitcoin, Ethereum, Solana, Cardano, Chainlink, Uniswap, Dogecoin, Render Token, Stacks e Axie Infinity.**

                    Nosso objetivo não é apenas fornecer números, mas ajudá-lo a entender o que eles significam. Este dashboard se destaca ao conectar dados a contextos, oferecendo uma visão mais clara 
                    e útil para quem está começando no universo das criptomoedas. É uma ferramenta criada para quem quer aprender, explorar e se familiarizar com um dos mercados mais dinâmicos e promissores 
                    da atualidade. **Explore, descubra e comece sua jornada com mais confiança!**
                ''')
            ], className='content-text')
        ], className='row-container'),

        # Seção Ferramentas colocada separadamente abaixo
        html.Div([
            html.P("Ferramentas", className='title'),
            html.Div([
                'Foi utilizado um dataset abrangendo dois anos (01/11/2022 - 22/01/2025) da API ',
                html.A('Polygon', href="https://polygon.io/", target="_blank", style={"color": "#0084d6", 'text-decoration': 'none'}),
                ' juntamente com técnicas de web scraping pela bibliotecva Python ', html.A('pygooglenews', href="https://github.com/kotartemiy/pygooglenews", target="_blank", style={"color": "#0084d6", 'text-decoration': 'none'}), ' para coletar dados de notícias diretamente do site da ',
                html.A('GoogleNews', href="https://news.google.com", target="_blank", style={"color": "#0084d6", 'text-decoration': 'none'}),
                '. O projeto utilizou a biblioteca Plotly para criar visualizações interativas e o framework Dash para construir o dashboard, ambos em Python.'
            ], className='content-text')
        ], className='row-container'),
        
        # Metadados do Projeto
        html.Div([
            html.Div([
                html.P("Metadados do Projeto", className='title')
            ]),
            html.Table([
                html.Tbody([
                    html.Tr([html.Td("Título"), html.Td("Plataforma Interativa para Visualização de Dados para criptomoedas: Preços, Volumes e Sentimento de mercado")]),
                    html.Tr([html.Td("Assunto"), html.Td("Criptomoeda;  análise de mercado; notícias; análise de sentimento")]),
                    html.Tr([html.Td("Fonte"), html.Td("Polygon, Google News")]),
                    html.Tr([html.Td("Descrição"), html.Td("A ferramenta tem como objetivo disponibilizar dados de criptomoedas através de gráficos e filtros interativos")]),
                    html.Tr([
                        html.Td("Criador"),
                        html.Td(
                            html.A("Sthefane Arissa Harada", href="https://www.linkedin.com/in/sthefane-harada/", target="_blank", style={'color': '#00bfff', 'text-decoration': 'none'})
                        )
                    ]),
                    html.Tr([html.Td("Colaborador"), html.Td("Lucas José De Souza")]),
                    html.Tr([html.Td("Data"), html.Td("09/04/2025")]),
                    html.Tr([html.Td("Formato"), html.Td("Ferramenta web em Python utilizando biblioteca Plotly e framework Dash")]),
                    html.Tr([html.Td("Idioma"), html.Td("PT")]),
                ])
            ], className='styled-table', style={"width": "100%"})
        ], className='row-container')

    ])
])
