import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, server
from apps import dashboard, dashboard2

csv = "mydatastore.csv"


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(id='page-content'),
    html.Div(id='page-content2'),
])

index_page = html.Div([
    html.Div(
    dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
    }),
    ),
    html.Div(
    dcc.Input(id="passw", type="text", placeholder="Enter Password",className="inputbox2",
    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
    }),
    ),
    html.Div(
    html.Button('Verify', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
    style={'margin-left':'45%','padding-top':'30px'}),
    html.Div([dcc.Input(id='submitmode', value = 0)
        ], style={'display':'none'})
    ])


@app.callback(
    Output('url', 'pathname'),
   [Input('verify', 'n_clicks')],
    [State('user', 'value'),
                State('passw', 'value')])
def update_output(n_clicks, uname, passw):
    print('update_output')
    li={'ljacob':'admin123'}
    if uname =='' or uname == None or passw =='' or passw == None:
        print('no user')
        return '/'
    elif uname not in li:
        print('incorrect user')
        return '/incorrect'
    elif li[uname]==passw:
        print('correct')
        return '/dashboard'
    else:
        print('else')
        return '/'


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
