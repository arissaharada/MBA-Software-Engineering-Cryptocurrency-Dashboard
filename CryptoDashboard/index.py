from dash import html, dcc, Input, Output
#import dash_bootstrap_components as dbc
from app import app, server
from apps import home, dashboard, data, sentiment_analysis

# Define layout principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Para capturar a URL atual

    # Layout principal
    html.Div(
        children=[
            # Menu lateral
    html.Div(
        [
            html.Div([
                html.A(
                    html.Img(src="/assets/cryptocurrency1.png"),
                    href="https://www.flaticon.com/free-icon/cryptocurrency_8389263",
                    target="_blank"
                ),
                html.H2("Criptomoedas"),
            ], className="sidebar-header"),
            html.Hr(),
            html.A([html.Div(["Introdução"], className='nav-link')], href="/", className="nav-link", id="home-link"),
            html.A([html.Div(["Dashboard"], className='nav-link')], href="/apps/dashboard", className="nav-link", id="dashboard-link"),
            html.A([html.Div(["Análise de Sentimentos"], className='nav-link')], href="/apps/sentiment_analysis", className="nav-link", id="about-link"),
            html.A([html.Div(["Data"], className='nav-link')], href="/apps/data", className="nav-link", id="data-link"),
        ],
        className="sidebar"
    ),

            # Conteúdo principal com header
            html.Div(
                children=[
                    html.Div(id="header", className="header"),
                    html.Div(id="page-content", className="content")
                ],
                style={'width': '85%'}
            )
        ],
        style={'display': 'flex'}
    )
])

# Callback para atualizar a classe dos links ativos no menu lateral
@app.callback(
    [Output("home-link", "className"),
     Output("dashboard-link", "className"),
     Output("about-link", "className"),
     Output("data-link", "className")],
    [Input("url", "pathname")]
)
def update_active_link(pathname):
    # Atualiza a classe dos links de acordo com a URL atual
    home_class = "nav-link active" if pathname == "/" else "nav-link"
    dashboard_class = "nav-link active" if pathname == "/apps/dashboard" else "nav-link"
    about_class = "nav-link active" if pathname == "/apps/sentiment_analysis" else "nav-link"
    data_class = "nav-link active" if pathname == "/apps/data" else "nav-link"
    return home_class, dashboard_class, about_class, data_class

# Callback para atualizar o header e o conteúdo da página
@app.callback(
    [Output("header", "children"),
     Output("page-content", "children")],
    [Input("url", "pathname")]
)
def update_content(pathname):
    if pathname == '/':
        return html.H1("Introdução"), home.layout
    elif pathname == '/apps/dashboard':
        return html.H1("Dashboard"), dashboard.layout
    elif pathname == '/apps/data':
        return html.H1("Dataset"), data.layout
    elif pathname == '/apps/sentiment_analysis':
        return html.H1("Análise de Sentimentos"), sentiment_analysis.layout
    else:
        return html.H1("Página não encontrada"), html.H3("Página não encontrada.")

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
    # app.run_server(debug=False, host='0.0.0.0', port=8060)