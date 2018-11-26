# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from dash.dependencies import Input, Output

now = str(datetime.now())[:10]

# http://docs.activestate.com/activepython/3.6/get/linux/
#
# export OMP_NUM_THREADS=1
# export USE_SIMPLE_THREADED_LEVEL3=1
#
# http://altbin.net/installing-python-modules-on-hostgator-shared-hosting-using-virtualenv
# wget https://files.pythonhosted.org/packages/4e/8b/75469c270ac544265f0020aa7c4ea925c5284b23e445cf3aa8b99f662690/virtualenv-16.1.0.tar.gz
# tar xvzf virtualenv-16.1.0.tar.gz
# python virtualenv-16.1.0/src/virtualenv.py ./env
# pip install dash dash_core_components dash_html_components pandas


def get_df_pufferspeicher(df_date):
    df = pd.read_json('http://s521193931.online.de/uvr1611/analogChart.php?date=' + df_date + '&id=2&period=day')
    # https://stackoverflow.com/questions/19231871/convert-unix-time-to-readable-date-in-pandas-dataframe
    df[0] = (pd.to_datetime(df[0], unit='s'))
    return df

def get_df_solar(df_date):
    df = pd.read_json('http://s521193931.online.de/uvr1611/analogChart.php?date=' + df_date + '&id=5&period=day')
    df[0] = (pd.to_datetime(df[0], unit='s'))
    return df

def get_df_heizung(df_date):
    df = pd.read_json('http://s521193931.online.de/uvr1611/analogChart.php?date=' + df_date + '&id=3&period=day')
    df[0] = (pd.to_datetime(df[0], unit='s'))
    return df

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H1(children='Super Heizung hier mit plotly.dash'),
    dcc.DatePickerSingle(
        id='date-picker-single',
        display_format='YYYY-MM-DD',
        date=now
    ),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pufferspeicher', value='tab-1'),
        dcc.Tab(label='Solar', value='tab-2'),
        dcc.Tab(label='Heizung', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(id='output-container-puffer')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div(id='output-container-solar')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Div(id='output-container-heizung')
        ])

@app.callback(
    dash.dependencies.Output('output-container-puffer', 'children'),
    [dash.dependencies.Input('date-picker-single', 'date')])
def update_output_tab4(date):
    if date is not None:
        date_string = str(datetime.strptime(date, '%Y-%m-%d'))[:10]
        df = get_df_pufferspeicher(date_string)

        return html.Div([
            dcc.Graph(
                id='heizung',
                figure={
                    'data': [
                        go.Scatter(x=df[0], y=df[1], name='Außentemperatur', mode='lines'),
                        go.Scatter(x=df[0], y=df[2], name='Speicher Kopf 1', mode='lines'),
                        go.Scatter(x=df[0], y=df[3], name='Speicher Kopf 2', mode='lines'),
                        go.Scatter(x=df[0], y=df[4], name='Speicher Kopf 3', mode='lines'),
                        go.Scatter(x=df[0], y=df[5], name='Speicher 5 Boden', mode='lines'),
                        go.Scatter(x=df[0], y=df[6], name='Specher 4 Mitte', mode='lines'),
                        go.Scatter(x=df[0], y=df[7], name='Raumtemp RASP', mode='lines'),

                    ],
                    'layout': go.Layout(
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Temperature'},
#                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                        legend={'x': 0, 'y': 1}
                    )
                }, animate=False, style={'height': '80vh', 'width': '80vw'}
            ),
        ])


@app.callback(
    dash.dependencies.Output('output-container-solar', 'children'),
    [dash.dependencies.Input('date-picker-single', 'date')])
def update_output_tab4(date):
    if date is not None:
        date_string = str(datetime.strptime(date, '%Y-%m-%d'))[:10]
        df = get_df_solar(date_string)

        return html.Div([
            dcc.Graph(
                id='heizung',
                figure={
                    'data': [
                        go.Scatter(x=df[0], y=df[1], name='VL Solar', mode='lines'),
                        go.Scatter(x=df[0], y=df[2], name='Drehzahl Ladepumpe', mode='lines'),
                        go.Scatter(x=df[0], y=df[3], name='Solarstrahlung', mode='lines'),
                        go.Scatter(x=df[0], y=df[4], name='Ladepumpe Solar', mode='lines'),
                    ],
                    'layout': go.Layout(
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Temperature/Rpm'},
#                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                        legend={'x': 0, 'y': 1}
                    )
                }, animate=False, style={'height': '80vh', 'width': '80vw'}
            ),
        ])

@app.callback(
    dash.dependencies.Output('output-container-heizung', 'children'),
    [dash.dependencies.Input('date-picker-single', 'date')])
def update_output_tab4(date):
    if date is not None:
        date_string = str(datetime.strptime(date, '%Y-%m-%d'))[:10]
        df = get_df_heizung(date_string)

        return html.Div([
            dcc.Graph(
                id='heizung',
                figure={
                    'data': [
                        go.Scatter(x=df[0], y=df[1], name='VL Heizung', mode='lines'),
                        go.Scatter(x=df[0], y=df[2], name='RL Heizung', mode='lines'),
                        go.Scatter(x=df[0], y=df[3], name='Raumtemp RASP', mode='lines'),
                        go.Scatter(x=df[0], y=df[4], name='Drehzahl Hzg', mode='lines'),
                        go.Scatter(x=df[0], y=df[5], name='Außentemperatur', mode='lines'),
                        go.Scatter(x=df[0], y=df[6], name='Mischer H auf', mode='lines'),
                        go.Scatter(x=df[0], y=df[7], name='Mischer H zu', mode='lines'),
                        go.Scatter(x=df[0], y=df[7], name='Heizungspumpe ein/aus', mode='lines'),
                    ],
                    'layout': go.Layout(
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Temperature/Rpm'},
#                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                        legend={'x': 0, 'y': 1}
                    )
                }, animate=False, style={'height': '80vh', 'width': '80vw'}
            ),
        ])


if __name__ == '__main__':
    app.run_server(debug=True)