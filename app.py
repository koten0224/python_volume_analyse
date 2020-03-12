import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pandas as pd
import plotly.graph_objs as go
import os
import sqlite3 as sql
import re
'''
使用dash將爬完之資料庫結果呈現在網頁上
網址:https://kotens-nltk.herokuapp.com/
'''
app = dash.Dash()

db = sql.connect('test.db')
cursor = db.cursor()
cursor.execute("select * from key_words where length(name)>1")
df = pd.DataFrame(columns = ['name','val','types'],data=cursor.fetchall())
db.close()

main_types = ['心情', '科技', '運動', '投資', '遊戲', 
         '學術', '閒聊', '生活', '娛樂', '政治']

app.layout = html.Div([
    html.H2(children='Chinese Natural Language analyze show with Dash'),
    dcc.Dropdown(
        id="types",
        options=[
            {'label': i, 'value': i} for i in main_types
        ],
        value=['政治'],
        multi=True
    ),
    dcc.Graph(id='key_words',
              animate=True
              )
])

@app.callback(
    dash.dependencies.Output('key_words', 'figure'),
    [dash.dependencies.Input('types', 'value')])

def update_figure(selected_continent):
        
    filtered_df = df
    for type in selected_continent:    
        filtered_df = filtered_df[filtered_df.types.str.contains(type)]
    main_type_list = []
    size_list = []
    type_val_list = []
    for name,val,types in filtered_df.values:
        type_val_dic={type:0 for type in selected_continent}
        for key in type_val_dic:
            type_val_dic[key] = int(
                    re.search('(?<='+key+':)\d+',types).group()
                    )
        main_type = max(type_val_dic , key=lambda x:type_val_dic[x])
        main_type_list.append(main_type)
        type_val = sum(type_val_dic.values())
        type_val_list.append(type_val)
        size = (type_val**1.2 / val)**5
        size_list.append(size)
    filtered_df['type_val'] = type_val_list
    filtered_df['size'] = size_list
    filtered_df['main_type'] = main_type_list
    sizeref = 2*max(size_list)/(100**2)*4
    filtered_df = filtered_df.sort_values('size',ascending=False).head(1000)
    
    traces = []
    for i in selected_continent:
        df_by_continent = filtered_df[filtered_df.main_type == i]
        traces.append(go.Scatter(
            x=df_by_continent['type_val'],
            y=df_by_continent['val'],
            text=df_by_continent['name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': df_by_continent['size'],
                'line': {'width': 0.5, 'color': 'white'},
                'sizeref': sizeref,
                'symbol': 'circle',
                'sizemode': 'area'
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Type(s) appearance'},
            yaxis={'title': 'Total appearance'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    port=int(os.environ.get('PORT',9454))
    app.run_server(host='0.0.0.0',debug=True,port=port)

