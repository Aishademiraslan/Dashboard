import dash

# app = dash.Dash(__name__)
dash.register_page(__name__, path='/')
layout = dash.html.Div(
    style={'height': '100vh', 'textAlign': 'center', 'paddingTop': '20vh'},
    children=[
        dash.html.H1(
            "xxx", ## Removed because it is confidential
            style={'color': '#FFFFFF'}
        ),
        dash.html.P(
            "For a cleaner future",
            style={'color': '#BBBBBB'}
        ),
        dash.html.Div([
            dash.html.A(
                dash.html.Button(
                    "Usage",
                    style={'backgroundColor': '#007BFF', 'color': '#FFFFFF', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer'}
                ),
                href="usage"
            ),
            dash.html.A(
            dash.html.Button(
                "Prognosis",
                style={'backgroundColor': '#007BFF', 'color': '#FFFFFF', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer'}
            ),
            href="prognosis"
            )
        ])
    ]
)
