from flask import Flask
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
from plotly.subplots import make_subplots
import random
import numpy as np

from preprocessing import page_view, page_route, visit, session_time, session_time_sum, visit_scale
from register import load, regis_sum, regis_scale
from datetime import datetime, timedelta

# Flask 애플리케이션 생성
server = Flask(__name__)

# Dash 애플리케이션 생성
app = Dash(__name__, server=server)

# 초기 데이터 생성
data1 = {'x': [1, 2, 3, 4, 5], 'y': [10, 11, 12, 13, 14]}
data2 = {'x': [1, 2, 3, 4, 5], 'y': [5, 4, 3, 2, 1]}


############################### 

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

new_df = visit(df[0])
# new_df = df[0]

now = datetime.now()

################################## 

df_filtered = new_df


font_style = {
    'family': 'Arial',   # 폰트 종류
    'size': 18,          # 폰트 크기
    'color': 'green',    # 폰트 색상
    # 'weight': 'bold'     # 폰트 굵기
}


bar_plot = px.bar(page_route(df[0]), x="일", y="사이트 세션", color="페이지 경로", barmode="group", title="전체 방문자 수 ")

# 폰트 설정
bar_plot.update_layout(
    title={
        'text': "전체 방문자 수",
        'font': font_style
    },
    xaxis=dict(
        title='일',
        title_font=dict(
            family='Arial',   # 폰트 종류
            size=14,          # 폰트 크기
            color='blue',      # 폰트 색상
            
        )
    ),
    yaxis=dict(
        title='사이트 세션',
        title_font=dict(
            family='Arial',   # 폰트 종류
            size=14,          # 폰트 크기
            color='red',       # 폰트 색상
            
        )
    )
)

fig_style = {
            'height': '800px',  # 그래프 높이
            'backgroundColor': '#f4f4f4',  # 배경색
            'margin': '20px',  # 여백
            'border': '1px solid #ddd'  # 테두리
        }

# 대시보드 레이아웃 생성
app.layout = html.Div([
    html.H1(
            children=[
                html.P(children="📈", className="header_emoji"),
                html.H1(children="Wix 랜딩 페이지 방문자 통계 Dashboard", className="header_title",),
                html.P(children="Temp", className="header_description",),
            ],
            className="header"),

    dcc.RangeSlider(
        id='x-axis-slider1',
        min=1,
        max=5,
        step=1,
        marks={i: str(i) for i in range(1, 6)},
        value=[1, 5],
    ),

    dcc.Graph(
        id='dynamic-graph',
        # 막대그래프
        # bar_fig = px.bar(df_filtered, x="일", y="사이트 세션", color="페이지 경로", barmode='group', title="사이트 세션", color_discrete_map={'/bigdata': '#08bdbd', '/java': '#ff9914', '/pm': '#29bf12'})
        figure = px.bar(df_filtered, x="일", y="사이트 세션", title="전체 방문자 수 ", barmode='group', color_discrete_map={'/bigdata': '#08bdbd', '/java': '#ff9914', '/pm': '#29bf12', '/post': '#29bf14'}, ),
        # figure=px.line(data1, x='x', y='y', title='그래프 1 초기'),
        style=fig_style
    ),

    dash_table.DataTable(
        id='table',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            # {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '사이트 세션', 'id': '사이트 세션'},
        ],
        data=df_filtered.to_dict('records'),
    ),
##############################
    dcc.Graph(
        id='dynamic-graph2',
        
        figure = bar_plot,
        
        style = fig_style
    ),

    dash_table.DataTable(
        id='table2',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '사이트 세션', 'id': '사이트 세션'},
        ],
        data=page_route(df[0]).to_dict('records'),
    ),
####################################
    dcc.Graph(
        id='dynamic-graph_big',
        
        figure = px.bar(df[1], x="일", y="사이트 세션", color="다음 조회 페이지", barmode="group", title="빅데이터 페이지 방문자 수"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_big',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '다음 조회 페이지', 'id': '다음 조회 페이지'},
            {'name': '사이트 세션', 'id': '사이트 세션'},
        ],
        data=df[1].to_dict('records'),
    ),
    
##########################################
    dcc.Graph(
        id='dynamic-graph_java',
        
        figure = px.bar(df[2], x="일", y="사이트 세션", color="다음 조회 페이지", barmode="group", title="풀스택 페이지 방문자 수"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_java',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '다음 조회 페이지', 'id': '다음 조회 페이지'},
            {'name': '사이트 세션', 'id': '사이트 세션'},
        ],
        data=df[2].to_dict('records'),
    ),

##############################################

    dcc.Graph(
        id='dynamic-graph_pm',
        
        figure = px.bar(df[3], x="일", y="사이트 세션", color="다음 조회 페이지", barmode="group", title="PM 페이지 방문자 수"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_pm',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '다음 조회 페이지', 'id': '다음 조회 페이지'},
            {'name': '사이트 세션', 'id': '사이트 세션'},
        ],
        data=df[3].to_dict('records'),
    ),

##############################################
    dcc.Graph(
        id='dynamic-graph_session',
        
        # figure = px.bar(session_time_sum(session_time(df[0])), x="일", y="평균 세션 소요 시간", color="페이지 경로", barmode="group", title="평균 세션 소요시간"),
        figure = px.bar(page_route(df[0]), x="일", y="평균 세션 소요 시간", color="페이지 경로", barmode="group", title="평균 세션 소요시간"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '평균 세션 소요 시간', 'id': '평균 세션 소요 시간'},
        ],
        data=page_route(df[0]).to_dict('records'),
    ),

###############################################
    dcc.Graph(
        id='dynamic-graph_session',
        
        figure = px.bar(session_time_sum(session_time(df[1])), x="일", y="평균 세션 소요 시간", title="빅데이터 평균 세션 소요시간"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            # {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '평균 세션 소요 시간', 'id': '평균 세션 소요 시간'},
        ],
        data=session_time_sum(session_time(df[1])).to_dict('records'),
    ),

###############################################
    dcc.Graph(
        id='dynamic-graph_session',
        
        figure = px.bar(session_time(df[1]), x="일", y="평균 세션 소요 시간", color="다음 조회 페이지", barmode="group", title="빅데이터 평균 세션 소요시간"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            {'name': '다음 조회 페이지', 'id': '다음 조회 페이지'},
            {'name': '평균 세션 소요 시간', 'id': '평균 세션 소요 시간'},
        ],
        data=session_time(df[1]).to_dict('records'),
    ),

###############################################
    
    dcc.Graph(
        id='dynamic-graph_session',
        
        figure = px.bar(session_time_sum(session_time(df[2])), x="일", y="평균 세션 소요 시간", title="풀스택 평균 세션 소요시간"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            # {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '평균 세션 소요 시간', 'id': '평균 세션 소요 시간'},
        ],
        data=session_time_sum(session_time(df[2])).to_dict('records'),
    ),

###############################################
    
    dcc.Graph(
        id='dynamic-graph_session',
        
        figure = px.bar(session_time_sum(session_time(df[3])), x="일", y="평균 세션 소요 시간", title="PM 평균 세션 소요시간"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '일', 'id': '일'},
            # {'name': '페이지 경로', 'id': '페이지 경로'},
            {'name': '평균 세션 소요 시간', 'id': '평균 세션 소요 시간'},
        ],
        data=session_time_sum(session_time(df[3])).to_dict('records'),
    ),

###############################################
    
    dcc.Graph(
        id='dynamic-graph_regis',
        
        figure = px.bar(regi_sum, x="날짜", y="합계", color = '과정', barmode = 'group', title="신청자 추이"),
        
        style=fig_style
    ),

    dash_table.DataTable(
        id='table_session',
        columns=[
            # {'name': col, 'id': col} for col in df_filtered.columns
            {'name': '날짜', 'id': '날짜'},
            {'name': '과정', 'id': '과정'},
            {'name': '합계', 'id': '합계'},
        ],
        data=regi_sum.to_dict('records'),
    ),

###############################################

    
])



regi_sum = regis_sum(regi)
regis_scale(regi)

# 그래프 업데이트 콜백 함수
# def update_figure(data, x_range):
#     # 슬라이더 값에 따라 그래프의 x축 범위 조절
#     filtered_data = {'x': data['x'][x_range[0] - 1:x_range[1]], 'y': data['y']}
    
#     # 새로운 데이터로 그래프 업데이트
#     figure = px.line(filtered_data, x='x', y='y', title='업데이트된 그래프')
    
#     return figure



# 그래프 1 업데이트 콜백 함수
# @app.callback(
#     Output('dynamic-graph1', 'figure'),
#     [Input('x-axis-slider1', 'value')]
# )
# def update_graph1(x_range1):
#     return update_figure(data1, x_range1)

# # 그래프 2 업데이트 콜백 함수
# @app.callback(
#     Output('dynamic-graph2', 'figure'),
#     [Input('x-axis-slider2', 'value')]
# )
# def update_graph2(x_range2):
#     return update_figure(data2, x_range2)



# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=2500)