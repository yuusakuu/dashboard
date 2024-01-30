import warnings
import calendar
import openpyxl
import numpy as np
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, dash_table

from preprocessing import page_view, visit, session_time, session_time_sum, visit_scale
from register import load, regis_sum, regis_scale


def date_to_str(date):
    if type(date)==np.datetime64:
        # date.astype(str)
        unix_epoch = np.datetime64(0, 's')
        one_second = np.timedelta64(1, 's')
        seconds_since_epoch = (date - unix_epoch) / one_second
        np_to_date = datetime.utcfromtimestamp(seconds_since_epoch).date()
        return np_to_date
    else:
        return date.strftime('%Y-%m-%d')
    

csv = './traffic_2023-06-01_2024-01-11.csv'
xlsx = '신청자 추이.xlsx'
df = page_view(csv)
# visit(df[0])
visit_df = visit(df[0])

session_time(df[2])
session_time_sum(session_time(df[2]))

regi = load(xlsx)
regi_sum = regis_sum(regi)
regis_scale(regi)

# new_df = visit(df[0])
new_df = df[0]

now = datetime.now()

data = [
    {'Name': 'John', 'Age': 25, 'City': 'New York'},
    {'Name': 'Jane', 'Age': 30, 'City': 'San Francisco'},
    {'Name': 'Bob', 'Age': 22, 'City': 'Chicago'},
]


app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

app.layout = html.Div([
    html.Span([html.Br(style={"line-height": "15"})]),
    html.H4(f'Wix 트래픽 {now.year}년 {now.month}월 {now.day}일 기준.', style={"margin-bottom" : "100px"}),
    html.Span([html.Br(style={"line-height": "40"})]),
    # RangeSlider 속성 : Allowed arguments: allowCross, className, count, disabled, dots, drag_value, 
    #                     id, included, loading_state, marks, max, min, persisted_props, persistence, 
    #                     persistence_type, pushable, step, tooltip, updatemode, value, vertical, verticalHeight
    dcc.RangeSlider(
        id='date-slider',
        min=0,
        max=len(new_df['일'].unique()) - 1,
        step=1,  # 1일 단위
        # marks={i: date_to_str((date)) for i, date in enumerate(sorted(new_df['일'].unique()))},
        value=[0, len(new_df['일'].unique()) - 1],
        verticalHeight=100
        # className = 'range-slider-style',
        # style={"backgroundColor":"gray", "height":"50px"},
    ),
    
    # dcc.Graph(id='site-session-graph'),
    # dcc.Graph(id='unique-visitors-graph'),
    dcc.Graph(id='fig'),

    dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'Name', 'id': 'Name'},
            {'name': 'Age', 'id': 'Age'},
            {'name': 'City', 'id': 'City'},
        ],
        data=data,
    ),

    dcc.RangeSlider(
        id='x-axis-slider2',
        min=0,
        max=len(new_df['일'].unique()) - 1,
        step=1,  # 1일 단위
        # marks={i: date_to_str((date)) for i, date in enumerate(sorted(new_df['일'].unique()))},
        value=[0, len(new_df['일'].unique()) - 1],
        verticalHeight=100
        # className = 'range-slider-style',
        # style={"backgroundColor":"gray", "height":"50px"},
    ),

    dcc.Graph(id='fig2',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [5, 4, 3, 2, 1], 'type': 'bar', 'name': '그래프 2'},
            ],
            'layout': {
                'title': '그래프 2'
            }
        }),

html.H4([
        dbc.Button("마케팅 지표 다운로드", 
                    id="btn_txt", 
                    style={"display":"block", 
                            "margin":"auto", 
                            # 'vertical-align': 'middle',
                            "fontSize":"20px", 
                            "color":"black"},
                    color="warning",
                    ),
        dcc.Download(id="download-text-index"),
    ])# ,style={"backgroundColor":'gray', "height":'10px'},
, 
])



def update_figure( n_clicks, selected_dates,):
    start_idx, end_idx = selected_dates

    dates = sorted(new_df['일'].unique())
    start_date = dates[start_idx]
    end_date = dates[end_idx]

    df_filtered = new_df[(new_df['일'] >= start_date) & (new_df['일'] <= end_date)]

    # 막대그래프
    # bar_fig = px.bar(df_filtered, x="일", y="사이트 세션", color="페이지 경로", barmode='group', title="사이트 세션", color_discrete_map={'/bigdata': '#08bdbd', '/java': '#ff9914', '/pm': '#29bf12'})
    bar_fig = px.bar(df_filtered, x="일", y="사이트 세션", title="방문자 수 ")
    bar_fig.update_layout()

    # line_fig = px.line(new_df['일'], x="일", y="페이지 조회", title="페이지 조회")
    line_fig2 = px.line(df_filtered, x="일", y="사이트 세션", title="사이트 세션")

    # 두 그래프를 한 공간에 표시
    bar_fig.add_traces(line_fig2.data)

    # 레이아웃 조절
    bar_fig.update_layout(title_text="Wix 트래픽", height=400, width=1200)

    if n_clicks is None:
        return bar_fig, None
    else:

        return bar_fig, dcc.send_file(f'/home/data/DH.xlsx')


@app.callback(
    # Output('site-session-graph', 'figure'),
    # Output('unique-visitors-graph', 'figure'),
    Output('fig','figure'),
    Output("download-text-index", "data"),
    Input('btn_txt', 'n_clicks'),
    Input('date-slider', 'value'),
)

def update_graph1(x_range1):
    return update_figure(data1, x_range1)



@app.callback(
    # Output('site-session-graph', 'figure'),
    # Output('unique-visitors-graph', 'figure'),
    Output('fig','figure'),
    Output("download-text-index", "data"),
    Input('btn_txt', 'n_clicks'),
    Input('date-slider', 'value'),
)

def update_graph2(x_range2):
    return update_figure(data2, x_range2)

    
if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=2500)