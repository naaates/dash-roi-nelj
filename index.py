import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, server
from apps import dashboard, dashboard2

csv = "mydatastore.csv"


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(id='page-content',style={'font-family':'arial'}),
    html.Div(id='page-content2',style={'font-family':'arial'}),
])

index_page = html.Div([
    html.Div(
    dcc.Input(id="username", type="text", placeholder="Enter Username",className="inputbox1",
    style={'margin-left':'32%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
    'font-size':'16px','border-width':'3px','border-color':'rgb(0,123,255)'
    }),
    ),
    html.Div(
    dcc.Input(id="password", type="password", placeholder="Enter Password",className="inputbox2",
    style={'margin-left':'32%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
    'font-size':'16px','border-width':'3px','border-color':'rgb(0,123,255)',
    }),
    ),
    html.Div(
    html.Button('Log-in', id='login', n_clicks=0, style={'border-width':'1px','font-size':'14px'}),
    style={'margin-left':'48%','padding-top':'30px'}),
    html.Div([dcc.Input(id='submitmode', value = 0)
        ], style={'display':'none'})
    ])


@app.callback(
    Output('url', 'pathname'),
   [Input('login', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')])
def update_output(n_clicks, username, password):
    print('update_output')
    admin={'ljacob':'admin123'}
    if username =='' or username == None or password =='' or password == None:
        print('no user')
        return '/incorrect'
    elif username not in admin:
        print('incorrect user')
        return '/incorrect'
    elif admin[username]==password:
        print('correct')
        return '/dashboard'
    else:
        print('else')
        return '/incorrect'


@app.callback(Output('page-content', 'children'),
              Output('page-content2', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/':
        return index_page, ""
    elif pathname == '/dashboard':
        print('goes here')
        return "",dashboard.get_dashboard_layout()
    elif pathname == '/incorrect':
        print('goes here')
        return index_page, dashboard2.get_dashboard2_layout()
    else:
        return index_page, ""

if __name__ == '__main__':
    app.run_server()
