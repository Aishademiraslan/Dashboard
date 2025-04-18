import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)


navbar = dash.html.Div([
            dash.html.A(
                dash.html.Button(
                    "Home",
                    style={'backgroundColor': '#007BFF', 'color': '#FFFFFF', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer'}
                ),
                href="/"
            ),
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

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ],
    className='dbc',
    fluid=True
)


# app.layout = dash.html.Div([
#     # dash.html.H1('WELCOME TO THE HOMEPAGE', style={'color', 'white'}),
#     dash.html.Div([
#         dash.html.Div(
#             dash.dcc.Link(f"{page['name']} - {page['path']}", href=page['relative_path'])
#         ) for page in dash.page_registry.values()
#     ]),
#     dash.page_container
# ])

# app.layout = dash.html.Div([
#     dash.dcc.Location(id='location'),
#     dash.html.Div(id='content')
# ])

# @dash.callback(
#     dash.Output('content', 'children'),
#     dash.Input('location', 'href')
#     )
# def update(href):
#     if href == None:
#         return 'Homepage'
#     elif href == '/usage':
#         return dash.html.Div('usage')

if __name__ == '__main__':
    app.run(debug=True)
