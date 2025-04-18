import datetime
import time

import dash
import plotly as plt
import pandas as pd

import data_intervals

dash.register_page(__name__)

common_table_style = {
    'width': '100%',
    'margin': 'auto',
    'border': '1px solid white',
    'border-radius': '10px',
    'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'overflow': 'hidden'
}

common_header_style = {
    'backgroundColor': '#333',
    'color': 'white',
    'textAlign': 'center',
    'fontWeight': 'bold',
    'fontSize': '14px'
}

common_data_style = {
    'backgroundColor': '#555',
    'color': 'white',
    'textAlign': 'center',
    'fontSize': '12px',
    'border': '1px solid white'
}

days = 1

pw = data_intervals.Power(str(datetime.date.today()), str(datetime.date.today()))
pw_df = pw.rack_power_sum(f'{days}d').reset_index()
pw_data = pw_df.to_dict('records')
pw_columns=[{"name": i, "id": i} for i in pw_df.columns if i != "Datetime"]

em = data_intervals.Emissions(str(datetime.date.today()), str(datetime.date.today()))
em_df = em.rack_emissions_sum(f'{days}d').reset_index()
em_data = em_df.to_dict('records')
em_columns=[{"name": i, "id": i} for i in em_df.columns if i != "Datetime"]

pc = data_intervals.Power_Costs(str(datetime.date.today()), str(datetime.date.today()))
pc_df = pc.rack_power_costs_sum(f'{days}d').reset_index()
pc_data = pc_df.to_dict('records')
pc_columns=[{"name": i, "id": i} for i in pc_df.columns if i != "Datetime"]

layout = dash.html.Div([
    dash.html.Div([
        dash.html.H2('Power Usage', style={'textAlign': 'center', 'color': 'white'}),
        ], style={'width': '33%', 'display': 'inline-block'}),
    dash.html.Div([
        dash.html.H2('CO2 Emissions', style={'textAlign': 'center', 'color': 'white'}),
        ], style={'width': '33%', 'display': 'inline-block'}),
    dash.html.Div([
        dash.html.H2('Power Costs', style={'textAlign': 'center', 'color': 'white'}),
        ], style={'width': '33%', 'display': 'inline-block'}),
    
    dash.html.Div([
        dash.dcc.Graph(id='power-chart', style={'backgroundColor': '#121212'})
    ], style={'width': '33%', 'display': 'inline-block'}),
    dash.html.Div([
        dash.dcc.Graph(id='emissions-chart', style={'backgroundColor': '#121212'})
    ], style={'width': '33%', 'display': 'inline-block'}),
    dash.html.Div([
        dash.dcc.Graph(id='power-costs-chart', style={'backgroundColor': '#121212'})
    ], style={'width': '33%', 'display': 'inline-block'}),
    
    dash.dcc.Dropdown(
        ['Pr Rack', 'Pr Group', 'Overall'],
        value = 'Pr Rack',
        style={'width': '150px'},
        searchable=False,
        clearable=False,
        id='grouping-dropdown'
    ),

    dash.dcc.DatePickerRange(
            min_date_allowed = datetime.date(2003, 1, 1),
            max_date_allowed = datetime.date.today(),
            initial_visible_month = datetime.date.today(),
            start_date = datetime.date.today() - datetime.timedelta(days = 1),
            end_date = datetime.date.today(),
            updatemode = 'bothdates',
            minimum_nights = 0,
            display_format = 'YYYY-MM-DD',
            style={'width': '50%'},
            id='date-picker'
    ),

    dash.html.Div([
        dash.html.Div([
            dash.html.H2(
                'Power Usage',
                style={'textAlign': 'center', 'color': 'white'}
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        dash.html.Div([
            dash.html.H2(
                'CO2 Emissions',
                style={'textAlign': 'center', 'color': 'white'}
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        dash.html.Div([
            dash.html.H2(
                'Power Costs',
                style={'textAlign': 'center', 'color': 'white'}
            ),
        ], style={'width': '33%', 'display': 'inline-block'}),
        dash.html.Div([
            dash.html.Button('CSV', id='download-power-btn'),
            dash.dash_table.DataTable(
                data=pw_data,
                columns=pw_columns,
                style_table=common_table_style,
                style_header = common_header_style,
                style_cell = {'minWidth': '150px', 'maxWidth': '100%'},
                style_data = common_data_style,
                id='power-table'
            ),
            dash.dcc.Download(id='download-power-csv')
        ], style={'width': '33%', 'display': 'inline-block'}),
        dash.html.Div([
            dash.html.Button('CSV', id='download-emissions-btn'),
            dash.dash_table.DataTable(
                data=em_data,
                columns=em_columns,
                style_table=common_table_style,
                style_header = common_header_style,
                style_cell = {'minWidth': '150px', 'maxWidth': '100%'},
                style_data = common_data_style,
                id='emissions-table'
            ),
            dash.dcc.Download(id='download-emissions-csv')
        ], style={'width': '33%', 'display': 'inline-block'}),
        dash.html.Div([
            dash.html.Button('CSV', id='download-power-costs-btn'),
            dash.dash_table.DataTable(
                data=pc_data,
                columns=pc_columns,
                style_table=common_table_style,
                style_header = common_header_style,
                style_cell = {'minWidth': '150px', 'maxWidth': '100%'},
                style_data = common_data_style,
                id='power-costs-table'
            ),
            dash.dcc.Download(id='download-power-costs-csv')
        ], style={'width': '33%', 'display': 'inline-block'}),
    ]),
])

@dash.callback(
    dash.Output('power-table', 'data'),
    dash.Output('power-table', 'columns'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_power_table(start_date, end_date, value):
    if start_date is not None and end_date is not None:
        pw = data_intervals.Power(start_date, end_date)
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if start != end:
            days = int(str(end - start)[:2])+1
        else:
            days = 1

        
        if value == "Pr Rack":
            df = pw.rack_power_sum(f'{days}d').reset_index()
        elif value == "Pr Group":
            df = pw.lab_prod_power(f'{days}d').reset_index()
        elif value == 'Overall':
            df = pw.combined_power(f'{days}d').reset_index()

        pw_data = df.to_dict('records')
        columns=[{"name": i, "id": i} for i in df.columns if i != "Datetime"]

        return pw_data, columns
    return dash.no_update

@dash.callback(
    dash.Output('emissions-table', 'data'),
    dash.Output('emissions-table', 'columns'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_emissions_table(start_date, end_date, value):
    if start_date is not None and end_date is not None:
        em = data_intervals.Emissions(start_date, end_date)
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if start != end:
            days = int(str(end - start)[:2])+1
        else:
            days = 1

        
        if value == "Pr Rack":
            df = em.rack_emissions_sum(f'{days}d').reset_index()
        elif value == "Pr Group":
            df = em.lab_prod_emissions(f'{days}d').reset_index()
        elif value == 'Overall':
            df = em.combined_emissions(f'{days}d').reset_index()

        em_data = df.to_dict('records')
        columns=[{"name": i, "id": i} for i in df.columns if i != "Datetime"]

        return em_data, columns
    return dash.no_update

@dash.callback(
    dash.Output('power-costs-table', 'data'),
    dash.Output('power-costs-table', 'columns'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_costs_table(start_date, end_date, value):
    if start_date is not None and end_date is not None:
        pc = data_intervals.Power_Costs(start_date, end_date)
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if start != end:
            days = int(str(end - start)[:2])+1
        else:
            days = 1

        if value == "Pr Rack":
            df = pc.rack_power_costs_sum(f'{days}d').reset_index()
        elif value == "Pr Group":
            df = pc.lab_prod_power_costs(f'{days}d').reset_index()
        elif value == 'Overall':
            df = pc.combined_power_costs(f'{days}d').reset_index()
        pc_data = df.to_dict('records')
        columns=[{"name": i, "id": i} for i in df.columns if i != "Datetime"]
        return pc_data, columns
    return dash.no_update

@dash.callback(
    dash.Output('power-chart', 'figure'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_power_graph(start_date, end_date, value):
    time_start = time.time()
    pw = data_intervals.Power(start_date, end_date)
    class_time = f"CLASS TIME TAKEN: {time.time() - time_start}"
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if start != end:
        days = int(str(end - start)[:2])+1
    else:
        days = 1
        
    if value == 'Pr Rack':
        dataframe_start = time.time()
        df = pw.rack_power_sum(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': ["Rack " + str(rack) for rack in df['Rack']],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#0072CE'}
                    } for col in df.columns if col != 'Rack'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nRACKS POWER:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    elif value == 'Pr Group':
        dataframe_start = time.time()
        df = pw.lab_prod_power(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': df['Rack_Group'],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#0072CE'}
                    } for col in df.columns if col != 'Rack_Group'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nENVIRONMENTS POWER:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    return dash.no_update

@dash.callback(
    dash.Output('emissions-chart', 'figure'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_emissions_graph(start_date, end_date, value):
    time_start = time.time()
    em = data_intervals.Emissions(start_date, end_date)
    class_time = f"CLASS TIME TAKEN: {time.time() - time_start}"
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if start != end:
        days = int(str(end - start)[:2])+1
    else:
        days = 1

    if value == 'Pr Rack':
        dataframe_start = time.time()
        df = em.rack_emissions_sum(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': ["Rack " + str(rack) for rack in df['Rack']],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#B9D9EB'}
                    } for col in df.columns if col != 'Rack'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nRACKS EMISSIONS:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    elif value == 'Pr Group':
        dataframe_start = time.time()
        df = em.lab_prod_emissions(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': df['Rack_Group'],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#B9D9EB'}
                    } for col in df.columns if col != 'Rack_Group'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nENVIRONMENTS EMISSIONS:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    return dash.no_update

@dash.callback(
    dash.Output('power-costs-chart', 'figure'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def update_power_costs_graph(start_date, end_date, value):
    time_start = time.time()
    pc = data_intervals.Power_Costs(start_date, end_date)
    class_time = f"CLASS TIME TAKEN: {time.time() - time_start}"
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if start != end:
        days = int(str(end - start)[:2])+1
    else:
        days = 1

    if value == 'Pr Rack':
        dataframe_start = time.time()
        df = pc.rack_power_costs_sum(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': ["Rack " + str(rack) for rack in df['Rack']],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#002F6C'}
                    } for col in df.columns if col != 'Rack'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nRACKS POWER COSTS:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    elif value == 'Pr Group':
        dataframe_start = time.time()
        df = pc.lab_prod_power_costs(f'{days}d').reset_index().drop('Datetime', axis=1)
        dataframe_time = f"DATAFRAME TIME TAKEN: {time.time() - dataframe_start}"
        if not df.empty:
            graphing_start = time.time()
            fig = {
                'data': [
                    {
                        'x': df['Rack_Group'],
                        'y': df[col],
                        'type': 'bar',
                        'name': col,
                        'marker': {'color': '#002F6C'}
                    } for col in df.columns if col != 'Rack_Group'
                ],
                'layout': {
                    'title': f'Energy Data Overview ({start_date} to {end_date})',
                    'plot_bgcolor': '#161A1D',
                    'paper_bgcolor': '#161A1D',
                    'font': {'color': 'white'}
                }
            }
            graphing_time = f"GRAPHING TIME TAKEN: {time.time()-graphing_start}"
            overall_time = f"TIME TAKEN: {time.time()-time_start} s."
            print(f"\nENVIRONMENTS POWER COSTS:\n{class_time}\n{dataframe_time}\n{graphing_time}\n{overall_time}")
            return fig
    return dash.no_update

@dash.callback(
    dash.Output('download-power-csv', 'data'),
    dash.Input('download-power-btn', 'n_clicks'),
    dash.Input('power-table', 'data'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def power_csv(n_clicks, data, start_date, end_date, value):
    if n_clicks is None or dash.ctx.triggered[0]['prop_id'].split('.')[0] != 'download-power-btn':
        return None
    df = pd.DataFrame(data)

    if 'Datetime' in df.columns:
        df = df.drop('Datetime', axis=1)
    return dash.dcc.send_data_frame(df.to_csv, filename=f'{value} Power {start_date} - {end_date}.csv', index=False)

@dash.callback(
    dash.Output('download-emissions-csv', 'data'),
    dash.Input('download-emissions-btn', 'n_clicks'),
    dash.Input('emissions-table', 'data'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def power_csv(n_clicks, data, start_date, end_date, value):
    if n_clicks is None or dash.ctx.triggered[0]['prop_id'].split('.')[0] != 'download-emissions-btn':
        return None
    df = pd.DataFrame(data)
    
    if 'Datetime' in df.columns:
        df = df.drop('Datetime', axis=1)
    return dash.dcc.send_data_frame(df.to_csv, filename=f'{value} CO2 Emissions {start_date} - {end_date}.csv', index=False)

@dash.callback(
    dash.Output('download-power-costs-csv', 'data'),
    dash.Input('download-power-costs-btn', 'n_clicks'),
    dash.Input('power-costs-table', 'data'),
    dash.Input('date-picker', 'start_date'),
    dash.Input('date-picker', 'end_date'),
    dash.Input('grouping-dropdown', 'value')
)
def power_csv(n_clicks, data, start_date, end_date, value):
    if n_clicks is None or dash.ctx.triggered[0]['prop_id'].split('.')[0] != 'download-power-costs-btn':
        return None
    df = pd.DataFrame(data)

    if 'Datetime' in df.columns:
        df = df.drop('Datetime', axis=1)
    return dash.dcc.send_data_frame(df.to_csv, filename=f'{value} Power Costs {start_date} - {end_date}.csv', index=False)
