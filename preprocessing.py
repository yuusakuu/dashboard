import pandas as pd

def page_view(csv):
    df = pd.read_csv(csv )


    # df['페이지 경로'].unique()

    df_nan = df['다음 조회 페이지'].fillna('nan')
    df['다음 조회 페이지'] = df_nan

    for i in range(len(df)):
        if df['페이지 경로'][i] == '/':
            df['페이지 경로'][i] = '/bigdata'

        if '/post' in df['페이지 경로'][i]:
            df['페이지 경로'][i] = '/post'

        if df['다음 조회 페이지'][i] == '/':
            df['다음 조회 페이지'][i] = '/bigdata'

        if '/post' in df['다음 조회 페이지'][i]:
            df['다음 조회 페이지'][i] = '/post'
        
        # if df['평균 세션 소요 시간'][i] == 'NaN':
        #     df['평균 세션 소요 시간'][i] = '0s'

    df = df.sort_values(by='일')

    df = df.fillna('1s')

    filtered_df = df[df['일'].str.startswith('2024')]

    df = filtered_df[4:]
    df = df.reset_index()

    # 세션 소요 시간 -> 시, 분 -> 초로 변경 
    for i in range(len(df['평균 세션 소요 시간'])):
        # print(df['일'][i])
        # print(df['평균 세션 소요 시간'][i])
        if 'h' in df['평균 세션 소요 시간'][i]:
            # print(int(df['평균 세션 소요 시간'][i].split('h')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('h')[1].split('m')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('m')[1].split('s')[0]))
            df['평균 세션 소요 시간'][i] = int(df['평균 세션 소요 시간'][i].split('h')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('h')[1].split('m')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('m')[1].split('s')[0])
        else :
            if 'm' in df['평균 세션 소요 시간'][i]:
                # print(df['일'][i])
                # print(int(df['평균 세션 소요 시간'][i].split('m')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('m')[1].split('s')[0]))
                df['평균 세션 소요 시간'][i] = int(df['평균 세션 소요 시간'][i].split('m')[0]) * 60 + int(df['평균 세션 소요 시간'][i].split('m')[1].split('s')[0])
            else : 
                # print(df['일'][i])
                # print(int(df['평균 세션 소요 시간'][i].split('s')[0]))
                df['평균 세션 소요 시간'][i] = int(df['평균 세션 소요 시간'][i].split('s')[0])

    for i in range(len(df)):
        df['평균 세션 소요 시간'][i] = df['평균 세션 소요 시간'][i] / 60

    # 과정 별 데이터 프레임 분류

    bigdata = df['페이지 경로'] == '/bigdata'
    java = df['페이지 경로'] == '/java'
    pm = df['페이지 경로'] == '/pm'
    blog = df['페이지 경로'] == '/blog'

    java_df = df[java]
    java_df = java_df.sort_values(by='일')
    # java_df_nan = java_df['다음 조회 페이지'].fillna('nan')
    # java_df['다음 조회 페이지'] = java_df_nan
    #java_df

    pm_df = df[pm]
    pm_df = pm_df.sort_values(by='일')
    # pm_df_nan = pm_df['다음 조회 페이지'].fillna('nan')
    # pm_df['다음 조회 페이지'] = pm_df_nan
    #pm_df

    blog_df = df[blog]
    blog_df = blog_df.sort_values(by='일')
    # pm_df_nan = pm_df['다음 조회 페이지'].fillna('nan')
    # pm_df['다음 조회 페이지'] = pm_df_nan

    bigdata_df = df[bigdata]
    bigdata_df = bigdata_df.sort_values(by='일')
    # bigdata_df_nan = bigdata_df['다음 조회 페이지'].fillna('nan')
    # bigdata_df['다음 조회 페이지'] = bigdata_df_nan
    # bigdata_df

    # bigdata_df[bigdata_df['다음 조회 페이지'] == '/blog']
    # bigdata_df[bigdata_df['다음 조회 페이지'] == '/java']
    # bigdata_df[bigdata_df['다음 조회 페이지'] == '/pm']
    # bigdata_df[bigdata_df['다음 조회 페이지'] == 'nan']

    bigdata_df = bigdata_df.reset_index()
    java_df = java_df.reset_index()
    pm_df = pm_df.reset_index()
    blog_df = blog_df.reset_index()
    
    return df, bigdata_df, java_df, pm_df, blog_df
# 전체 페이지 조회, 사이트 세션, 고유 방문자 구하기 
# df = df, bigdata_df, java_df, pm_df

def page_route(df):
    day = list(df['일'].unique())
    view = []
    page_url = ['/pm', '/java', '/bigdata', '/post', '/blog']

    for i in range(len(day)):
        for j in range(len(page_url)):
            view_sum = 0
            session_sum = 0
            visitor = 0
            session_time = 0

            result = df[df['일'] == day[i]][df[df['일'] == day[i]]['페이지 경로'] == page_url[j]]
            result = result.reset_index()
            
            if len(result) == 0:
                pass
            else :
                for k in range(len(result)):
                    view_sum += result['페이지 조회'][k]
                    session_sum += result['사이트 세션'][k]
                    visitor += result['고유 방문자'][k]

                    session_time += result['평균 세션 소요 시간'][k] * result['사이트 세션'][k] 

                session_time_avg = session_time / view_sum
                view.append([day[i], page_url[j], view_sum, session_sum, visitor, session_time_avg])
    
    page = pd.DataFrame(view)
    page.columns = ['일', '페이지 경로','페이지 조회', '사이트 세션', '고유 방문자', '평균 세션 소요 시간']
    return page




def visit(df):
    # df = df.reset_index()
    day = []
    sum = 0

    for i in range(len(df)-1):
        if df['일'][i] == df['일'][i+1]:
            sum += df['페이지 조회'][i]
        else :
            sum += df['페이지 조회'][i]
            day.append(df['일'][i])
            sum = 0
        if i+2 == len(df):
            # print('last')
            sum += df['페이지 조회'][i+1]
            day.append(df['일'][i+1])

    page_view = []
    sum = 0

    for i in range(len(df)-1):
        if df['일'][i] == df['일'][i+1]:
            sum += df['페이지 조회'][i]
        else :
            sum += df['페이지 조회'][i]
            page_view.append(sum)
            sum = 0
        if i+2 == len(df):
            sum += df['페이지 조회'][i+1]
            page_view.append(sum)

    site_session = []
    sum = 0

    for i in range(len(df)-1):
        if df['일'][i] == df['일'][i+1]:
            sum += df['사이트 세션'][i]
        else :
            sum += df['사이트 세션'][i]
            site_session.append(sum)
            sum = 0
        if i+2 == len(df):
            sum += df['사이트 세션'][i+1]
            site_session.append(sum)

    visitor = []
    sum = 0

    for i in range(len(df)-1):
        if df['일'][i] == df['일'][i+1]:
            sum += df['고유 방문자'][i]
        else :
            sum += df['고유 방문자'][i]
            visitor.append(sum)
            sum = 0
        if i+2 == len(df):
            sum += df['고유 방문자'][i+1]
            visitor.append(sum)

    visit_df = pd.DataFrame(day)
    visit_df.columns = ['일']
    visit_df['페이지 조회'] = page_view
    visit_df['사이트 세션'] = site_session
    visit_df['고유 방문자'] = visitor
    # visit_df
    return visit_df

# 세션 소요 시간 초 변환
def session_time(df):
    # df = df.reset_index()
    session_time = [ ]
    session_sum = 0 
    for i in range(1, len(df)-1):
            
        if df['일'][i+1] ==  df['일'][i] :
            session_sum += df['평균 세션 소요 시간'][i]
            # print( df['일'][i] )
        else :
            session_sum += df['평균 세션 소요 시간'][i]
            session_time.append([ df['일'][i-1], session_sum])
            session_sum = 0
            
        if i+1 == len(df):
            session_sum += df['평균 세션 소요 시간'][i]
            session_time.append([ df['일'][i-1], session_sum])
            session_sum = 0


    return df

# 전체 세션 소요 시간 통합 
def session_time_sum(df):
        
    # session_time = [ ]
    # session_sum = 0 
    # for i in range(1, len(df)-1):
    #     cnt = 0
    #     if df['일'][i+1] ==  df['일'][i] :
    #         session_sum += df['평균 세션 소요 시간'][i]
    #         cnt += 1
    #     else :
    #         if cnt > 0 :
    #             session_sum += df['평균 세션 소요 시간'][i]
    #             session_time.append([ df['일'][i-1], session_sum])
    #             session_sum = 0
    #         else :
    #             session_sum += df['평균 세션 소요 시간'][i]
    #             session_time.append([ df['일'][i], session_sum])
    #             session_sum = 0
            
    #     if i+1 == len(df):
    #         if cnt > 0 :
    #             session_sum += df['평균 세션 소요 시간'][i]
    #             session_time.append([ df['일'][i-1], session_sum])
    #             session_sum = 0
    #         else :
    #             session_sum += df['평균 세션 소요 시간'][i]
    #             session_time.append([ df['일'][i], session_sum])
    #             session_sum = 0

    # session = pd.DataFrame(session_time)
    # session.columns = ['일', '평균 세션 소요 시간'] 
    session_time = [ ]
    session_sum = 0 

    for i in range(len(df)-1):
        if df['일'][i] == df['일'][i+1]:
            session_sum += df['평균 세션 소요 시간'][i]
        else :
            session_sum += df['평균 세션 소요 시간'][i]
            session_time.append([df['일'][i], session_sum])
            session_sum = 0
        if i+2 == len(df):
            session_sum += df['평균 세션 소요 시간'][i+1]
            session_time.append([df['일'][i], session_sum])

    session = pd.DataFrame(session_time)
    session.columns = ['일', '평균 세션 소요 시간']
    return session


def visit_scale(df):
    df_scale = df.copy()
    df_scale['페이지 조회'] = df['페이지 조회'] / df['페이지 조회'].max()
    df_scale['사이트 세션'] = df['사이트 세션'] / df['사이트 세션'].max()
    df_scale['고유 방문자'] = df['고유 방문자'] / df['고유 방문자'].max()
    return df_scale