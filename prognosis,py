import datetime

import dash
import plotly as plt
import pandas as pd

import data_intervals

dash.register_page(__name__)

days = 1
pw = data_intervals.Power(str(datetime.date.today()), str(datetime.date.today()))
pw_df = pw.rack_power().reset_index()
pw_data = pw_df.to_dict('records')
pw_columns = [{'name': i, 'id': i} for i in pw_df.columns]
data_points = ['Laboratory', 'Production']
racks = ["Rack " + str(rack) for rack in pw_df['Rack'].unique()]
for rack in racks:
    data_points.append(rack)

em = data_intervals.Emissions(str(datetime.date.today()), str(datetime.date.today()))
em_df = em.rack_emissions().reset_index()
em_data = em_df.to_dict('records')
em_colums = [{'name': i, 'id': i} for i in em_df.columns]

pc = data_intervals.Power_Costs(str(datetime.date.today()), str(datetime.date.today()))
pc_df = pc.rack_power_cost_avg().reset_index()
pc_data = pc_df.to_dict('records')
pc_columns = [{'name': i, 'id': i} for i in pc_df.columns]

layout = dash.html.Div([
    dash.html.H1('Welcome to the Prognosis Page', style={'color': 'white'}),
    dash.dcc.Graph(id = 'prognosis-chart', style={'backgroundColor': 'black'}),
    dash.dcc.Dropdown(
        id = 'data-type-picker',
        options = ['Power Usage', 'CO2 Emissions', 'Power Costs'],
        value = 'Power Usage',
        style = {'width': '150px'},
        searchable = False,
        clearable = False
    ),
    dash.dcc.Dropdown(
        id = 'rack-picker',
        options = data_points,
        value = 'Laboratory',
        style = {'width': '150px'},
        searchable = False,
        clearable = False
    ),
    # dash.dcc.Store(id='date-storage', storage_type='session'),
    dash.dcc.DatePickerSingle(
        id = 'prognosis-date-picker',
        min_date_allowed = datetime.date(2003, 1, 1),
        max_date_allowed = datetime.date.today(),
        initial_visible_month = datetime.date.today(),
        date = datetime.date.today(),
        display_format = 'YYYY-MM-DD'
    )
])



@dash.callback(
    dash.Output('prognosis-chart', 'figure'),
    dash.Input('prognosis-date-picker', 'date'),
    dash.Input('data-type-picker', 'value'),
    dash.Input('rack-picker', 'value')
)
def prognosis_chart(date, type_value, data_point):
    if type_value == 'Power Usage':
        data_class = data_intervals.Power(date, date)
        if data_point != 'Laboratory' and data_point != 'Production':
            df = data_class.rack_power().reset_index()
            
            df_all = data_class.rack_power(all=True).reset_index()
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack', 'Hour'])['VA (Wh)'].mean().reset_index()
        else:
            df = data_class.lab_prod_power('h').reset_index()
            df = df[df['Rack_Group'] == data_point]

            df_all = data_class.lab_prod_power('h', all=True).reset_index()
            df_all = df_all[df_all['Rack_Group'] == data_point]
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack_Group', 'Hour'])['VA (Wh)'].mean().reset_index()

    elif type_value == "CO2 Emissions":
        data_class = data_intervals.Emissions(date, date)
        if data_point != 'Laboratory' and data_point != 'Production':
            df = data_class.rack_emissions().reset_index()

            df_all = data_class.rack_emissions(all=True).reset_index()
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack', 'Hour'])['CO2 Grams'].mean().reset_index()
        else:
            df = data_class.lab_prod_emissions('h').reset_index()
            df = df[df['Rack_Group'] == data_point]

            df_all = data_class.lab_prod_emissions('h', all=True).reset_index()
            # print(f"{df_all = }")
            df_all = df_all[df_all['Rack_Group'] == data_point]
            # print(f"{df_all = }")
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack_Group', 'Hour'])['CO2 Grams'].mean().reset_index()


    elif type_value == "Power Costs":
        data_class = data_intervals.Power_Costs(date, date)
        # print(data_point)
        if data_point != 'Laboratory' and data_point != 'Production':
            df = data_class.rack_power_cost_avg().reset_index()

            df_all = data_class.rack_power_cost_avg(all=True).reset_index()
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack', 'Hour'])['Power Costs DKK'].mean().reset_index()
        else:
            df = data_class.lab_prod_power_costs('h').reset_index()
            # print(f"{df = }")
            df = df[df['Rack_Group'] == data_point]

            df_all = data_class.lab_prod_power_costs('h', all=True).reset_index()
            df_all = df_all[df_all['Rack_Group'] == data_point]
            # print(f"{df_all = }")
            df_all['Hour'] = df_all['Datetime'].dt.hour
            df_all = df_all.drop('Datetime', axis=1)
            df_prognosis = df_all.groupby(['Rack_Group', 'Hour'])['Power Costs DKK'].mean().reset_index()
            # print(f"{df_prognosis = }")

    if not df.empty:
        if data_point != 'Laboratory' and data_point != 'Production':
            df_filtered = df[df['Rack'] == int(data_point[5])]
            # print(df_filtered)
            df_prog_filtered = df_prognosis[df_prognosis['Rack'] == int(data_point[5])]
            prog_value_col = [col for col in df_prog_filtered.columns if col not in ['Hour', 'Rack']][0]
            # print(f"{df_prog_filtered = }")
        else:
            df_filtered = df
            df_prog_filtered = df_prognosis
            prog_value_col = [col for col in df_prog_filtered.columns if col not in ['Hour', 'Rack_Group']][0]
            # print(f"{df_prog_filtered = }")
        
        if type_value == 'CO2 Emissions':
            min_val = 0
            max_val = df_prog_filtered[prog_value_col].max() + (float(df_prog_filtered[prog_value_col].max()))
        elif type_value == 'Power Costs':
            min_val = df_prog_filtered[prog_value_col].min() - (float(df_prog_filtered[prog_value_col].min()))
            max_val = df_prog_filtered[prog_value_col].max() + (float(df_prog_filtered[prog_value_col].max()))
        else:
            min_val = df_prog_filtered[prog_value_col].min() - (float(df_prog_filtered[prog_value_col].min())*0.5)
            max_val = df_prog_filtered[prog_value_col].max() + (float(df_prog_filtered[prog_value_col].max())*0.5)
        
        if data_point != 'Laboratory' and data_point != 'Production':
            data_point_type = 'Rack'
        else:
            data_point_type = 'Rack_Group'

        fig = {
            'data': [
                {
                    'x': [str(timestamp) for timestamp in df_filtered['Datetime']],
                    'y': df_filtered[col],
                    'type': 'line',
                    'name': col,
                    'marker': {'color': '#1283D2'}
                } for col in df_filtered.columns if col not in ['Datetime', data_point_type]
            ] + [
                {
                    'x': [f'{date} {hour:02d}:00' for hour in df_prog_filtered['Hour']],
                    'y': df_prog_filtered[prog_value_col],
                    'type': 'line',
                    'name': f'{prog_value_col}: Prognosis',
                    'line': {'dash': 'dash', 'color': '#56A08A'},
                    'mode': 'lines'
                }
            ],
            'layout':{
                'title': f'{type_value} Daily Overview',
                'plot_bgcolor': '#161A1D',
                'paper_bgcolor': '#161A1D',
                'font': {'color': '#E0E0E0'},
                'xaxis': {'range': [f'{date} 00:00', f'{date} 23:59'], 'tickformat': '%H:%M', 'gridcolor': '#333333', 'tickcolor': '#B0B0B0'},
                'yaxis': {'range': [min_val, max_val]}
            }
        }
        return fig
    return dash.no_update
