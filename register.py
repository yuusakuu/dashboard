import pandas as pd
import openpyxl as op

def load(xlsx):
    
    workbook = op.load_workbook(xlsx, data_only=True)
    sheet_list = [sheet.title for sheet in workbook]

    data = workbook[sheet_list[0]].values

    col = []
    for i in range(len(workbook[sheet_list[0]][2])):
        col.append(workbook[sheet_list[0]][2][i].value) 


    regis = pd.DataFrame(data, columns = col)
    regis = regis[2:].fillna(0)
    

    for i in range(2, len(regis)+1):
        if len(str(regis['날짜'][i].month)) == 1 :
            month = '0'+ str(regis['날짜'][i].month)
            type(month)
        else : month = str(regis['날짜'][i].month)
        if len(str(regis['날짜'][i].day)) == 1 :
            day = '0' + str(regis['날짜'][i].day)
        else :
            day = str(regis['날짜'][i].day)
        regis['날짜'][i] = str(regis['날짜'][i].year) + '-' + month + '-' + day
    
    regis = regis[:-1]
    return regis


def regis_sum(df):
    regi_big = pd.DataFrame(df[['날짜','빅데이터']])
    regi_java = pd.DataFrame(df[['날짜','풀스택']])
    regi_pm = pd.DataFrame(df[['날짜','PM']])

    regi_big.columns =['날짜','합계']
    regi_java.columns =['날짜','합계']
    regi_pm.columns =['날짜','합계']

    regi_big['과정'] = '빅데이터'
    regi_java['과정'] = '풀스택'
    regi_pm['과정'] = 'PM'

    regi_sum = pd.concat((regi_big, regi_java, regi_pm))
    regi_sum = regi_sum.reset_index()

    return regi_sum



def regis_scale(df):
    big_max = df['빅데이터'].max()
    java_max = df['풀스택'].max()
    pm_max = df['PM'].max()
    sum_max = df['합계'].max()
    sum2_max = df['누적합계'].max()
    
    regi_new = df.copy()

    regi_new['빅데이터'] = df['빅데이터'] / big_max
    regi_new['풀스택'] = df['풀스택'] / java_max
    regi_new['PM'] = df['PM'] / pm_max
    regi_new['합계'] = df['합계'] / sum_max
    regi_new['누적합계'] = df['누적합계'] / sum2_max
    
    return regi_new 



