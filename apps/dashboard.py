import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import base64
import numpy as np
import sqlite3
from dash.exceptions import PreventUpdate
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

from app import app

# Add dashboard specific methods here

def get_dashboard_layout():

    # Call dashboard specific methods here

    return [
        html.Div([
        html.Div(dcc.Link('Log out', href='/',style={'color':'#FFFFFF', 'font-weight': 'bold', 'font-size':'16px',"text-decoration": "none",}),style={'padding-left':'92%','padding-top':'10px', 'background-color':'rgb(0,123,255)'}),
        ]),
        html.Div([

        
        html.Div([
                html.Div([
                        html.H2("Return of Investments Inputs:", style = {'color':'rgb(0,123,255)', 'font':'Verdana'}),
                        html.Table([
                                html.Tr(children = [html.Td("Scenario Name:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'scenarioname', type='text', value = 'Scenario 1', style = {'fontSize': 20}))]),                            
                                html.Tr(children = [html.Td("Total Hits:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'totalHits', type='number', value = 1000000, style = {'fontSize': 20}))]),
                               
                                html.Tr(children = [html.Td("Conversion Rate:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'conversionRate', type='number', value = 60, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Revenue Per Purchase (PhP):", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'revenuePerPurchase', type='number', value = 50, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Number of Times of Purchase per Converted User per Year:", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'ntpcuy', type='number', value = 2, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("Total Cost of Sampling (PhP):", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'samplingCost', type='number', value = 25000000, style = {'fontSize': 20})
                                                            )]),
                                html.Tr(children = [html.Td("% of Potential Revenue You are willing to allocate for sampling", className='lined', style={'width': '50%'}),
                                                    html.Td(dcc.Input(id = 'potentialRevenue', type='number', value = 50, style = {'fontSize': 20})
                                                            )]),
                        ], style = {'width':'100%'}),
                        html.Hr(),
                        html.Button(id = 'submitButton',
                            children = 'Calculate ROI',
                            n_clicks = 0, className='btn btn-primary btn',
                            style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                            ),
                        html.Hr(),
                        html.Table([        
                            html.Tr([
                                html.Td([
                                    "Select Scenario:"
                                    ], style={'width': '50%'}),
                                html.Td([
                                    dcc.Dropdown( id = "ddselectscenario")
                                    ], style={'width': '50%'})                                
                                ]),
                            html.Tr([                            
                                 html.Td([
                                    html.Button(id = 'saveButton',
                                        children = 'Save Settings',
                                        n_clicks = 0, className='btn btn-primary btn',
                                        style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                                        ),
                                ]),
                                html.Td([
                                    dcc.Checklist(
                                        options=[
                                            {'label': 'Edit Mode', 'value': 1},
                                        ],
                                        id="mode",
                                        value=[],
                                        labelStyle={'display': 'inline-block'}
                                    )
                                                                     
                                ]),
                            ]),
                            html.Tr([
                                 html.Td([
                                    html.Button(id = 'deleteButton',
                                        children = 'Delete This Scenario',
                                        n_clicks = 0, className='btn btn-primary btn',
                                        style = {'fontSize': '15px', 'color':'white', 'background-color':'rgb(0,123,255)', 'float':'middle', 'border-radius':'5px', 'border':'5px'}
                                        ),
                                     
                                ])                                
                             ]),
                        ], style = {'width':'100%'}),
                                
                ], style = {'width':'30%', 'display':'inline-block', 'float':'left', 'marginTop':'0px'}),

                html.Div([
                        html.H2(children='Investment/Income Breakdown:', style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana'}),
                        dcc.Graph(id = 'donut', style = {'height':300}, config = {
                                          'displayModeBar':False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                        html.H2(children='ROI Parameters Computed:', style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                        html.Table([
                                html.Tr(children = [html.Td("Total Potential Annual Revenue",
                                                className='lined', style={'width': 150, 'border':'1px solid black', 'fontSize':15}),
                                                html.Td(html.Div(id = 'tparOutput', style = {'float':'right'}),
                                                className='lined', style={'width': 200, 'border':'1px solid black'})
                                        ], style = {'height':'10%'}),
                                html.Tr(children = [html.Td("Unconverted Opportunity Revenue",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'uorOutput', style = {'float':'right'}),
                                                        className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Converted Revenue",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'convertedRev', style = {'float':'right'})
                                                        , className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Maximum Allowable Spend",
                                                        className='lined', style={'width': 150, 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'MaxAllowSpend', style = {'float':'right'})
                                                        , className='lined', style={'width': 200, 'border':'1px solid black'})
                                                ]),
                                html.Tr(children = [html.Td("Maximum Spend per Hit",
                                                        className='lined', style={'width': '60%', 'border':'1px solid black'}),
                                                html.Td(html.Div(id = 'MaxSpendPerHit', style = {'float':'right'})
                                                        , className='lined', style={'width': '40%', 'border':'1px solid black'})
                                                ])
                                    ], style = {'border-collapse':'collapse', 'width':'100%'}),
                        html.H2(children = "Estimated Net Profit From Sampling:", style = {'color':'rgb(0,123,255)', 'font':'Verdana', 'textAlign':'center'}),
                        html.Table([
                                html.Tr(children = [html.Td("Net Profit",
                                                className='lined', style={'width': '30%', 'border':'1px solid black'}),
                                        html.Td(html.Div(id = 'netProfit', style = {'float':'right'})
                                                , className='lined', style={'width': '70%', 'border':'1px solid black'})
                                        ])
                                ], style ={'border-collapse':'collapse', 'width':'100%'})
                ], className='cmd', style = {'width':'35%', 'display':'inline-block','float':'left'}),

                html.Div([
                        html.H2("Waterfall Chart", style = {'textAlign':'center', 'color':'rgb(0,123,255)', 'font':'Verdana', 'height':'10vh'}),
                        dcc.Graph(id = 'waterfall',
                                  config = {
                                          'displayModeBar':False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']})
                ], style = {'width':'35%', 'display':'inline-block', 'float':'right'})
            ])
        ])
        
    ]

# TPAR
@app.callback(
        [Output('tparOutput', 'children'),
         Output('uorOutput', 'children')
         ],
        [Input('submitButton', 'n_clicks')],
        [State('totalHits', 'value'),
         State('revenuePerPurchase', 'value'),
         State('ntpcuy','value'),
         State('conversionRate', 'value')])
def output1(n_clicks, totalHits, revenuePerPurchase, ntpcuy, conversionRate):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    tpar1 = '{:,.2f}'.format(tpar)
    uor = (1 - float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))
    uor1 = '{:,.2f}'.format(uor)
    return ["Php {}".format(tpar1), "Php {}".format(uor1)]

# Converted Revenue
@app.callback(
        Output('convertedRev', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value')])
def output3(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy):
    cr = (float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))
    cr1 = '{:,.2f}'.format(cr)
    return "Php {}".format(cr1)

# Maximum Allowable Spend
@app.callback(
        Output('MaxAllowSpend', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def output4(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    mas = (((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)) * float(potentialRevenue)/100
    mas1 = '{:,.2f}'.format(mas)
    return "Php {}".format(mas1)


# Maximum Allowable Spend Per Hit
@app.callback(
        Output('MaxSpendPerHit', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def output5(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    masph = ((((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)) * float(potentialRevenue)/100)/float(totalHits)
    masph1 = '{:,.2f}'.format(masph)
    return "Php {}".format(masph1)

# Net Profit
@app.callback(
        Output('netProfit', 'children'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value')])
def output6(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost):
    np = ((float(conversionRate)/100) * (float(totalHits) * float(revenuePerPurchase) * float(ntpcuy))) - float(samplingCost)
    np1 = '{:,.2f}'.format(np)
    return "Php {}".format(np1)

# For Waterfall Chart
@app.callback(
        Output('waterfall', 'figure'),
        [Input('submitButton', 'n_clicks')],
        [State('conversionRate', 'value'),
        State('totalHits', 'value'),
        State('revenuePerPurchase', 'value'),
        State('ntpcuy','value'),
        State('samplingCost', 'value'),
        State('potentialRevenue', 'value')])
def waterfall(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    uor = np.abs((1 - float(conversionRate)/100) * tpar)
    convertedRev = (float(conversionRate)/100) * tpar
    netProfit = convertedRev - float(samplingCost)
    netProfitNFS = np.abs((1 - float(potentialRevenue)/100) * netProfit)
    MaxAllowSpend = (float(potentialRevenue)/100) * netProfit

    fig = {
            'data': [
                    {'labels':['tpar','uor'],
                     'x':['Total Potential Annual Revenue', 'Unconverted Opportunity Revenue'],
                     'y':[tpar,-uor],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                     {'labels':['tcs','uor'],
                      'x':['Converted Revenue', 'Sampling Cost'],
                      'y':[convertedRev,-float(samplingCost)],
                      'type':'waterfall',
                      'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                    {'labels':['tcs','uor'],
                     'x':['Net Profit', 'Net Profit Not For Sampling'],
                     'y':[netProfit,-netProfitNFS],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}},
                    {'labels':['tcs'],
                     'x':['Max Allowable Spend'],
                     'y':[MaxAllowSpend],
                     'type':'waterfall',
                     'increasing':{'marker':{'color':'rgba(44, 82, 103, 0.70)'}},
                     'decreasing':{'marker':{'color':'rgba(255, 59, 60, 0.70)'}},
                     'connector': {'visible':False}}
                    ],
    'layout': {'showlegend': False,
               'xaxis':{'automargin':True, 'title':'ROI Parameters'},
               'margin':dict(t = 0)
            }}
    return fig

@app.callback(
         Output('donut', 'figure'),
         [Input('submitButton', 'n_clicks')],
         [State('conversionRate', 'value'),
          State('totalHits', 'value'),
          State('revenuePerPurchase', 'value'),
          State('ntpcuy','value'),
          State('samplingCost', 'value'),
          State('potentialRevenue', 'value')])
def donutchart(n_clicks, conversionRate, totalHits, revenuePerPurchase, ntpcuy, samplingCost, potentialRevenue):
    tpar = float(totalHits) * float(revenuePerPurchase) * float(ntpcuy)
    uor = (1 - float(conversionRate)/100) * tpar
    convertedRev = (float(conversionRate)/100) * tpar
    netProfit = convertedRev - float(samplingCost)
    netProfitNFS = (1 - float(potentialRevenue)/100) * netProfit
    MaxAllowSpend = (float(potentialRevenue)/100) * netProfit
    a = ['Unconverted Revenue', 'Sampling Cost', 'Max Allowable Spend', 'Net Profit Not For Sampling']
    b = [uor, samplingCost, MaxAllowSpend, netProfitNFS]

    fig = { "data": [
    {
      "values": b,
      "labels": a,
      "marker": {
              'colors':['rgb(242, 217, 187)',
              'rgb(44,82,103)',
              'rgb(134, 169, 189)',
              'rgb(255, 59, 60)'],
                'line':{'colors':['rgba(1,1,1,0)'], 'width': 2}
              },
      "hoverinfo":"label+percent",
      "hole": .4,
      "type": "pie",
      'textposition':'outside',
      'outsidetextfont':{"size":11},
      "textinfo":"label+value"
    }],
    'layout': {#'title': 'Investment or Income Breakdown',
               'showlegend': False,
               'margin':dict(t = 0)},
            'config':{
                    'displayModeBar':False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
}
    return fig



@app.callback(
         [Output('ddselectscenario', 'options'),
          Output('ddselectscenario', 'value'),
          ],
         [
             Input('saveButton', 'n_clicks'),
             Input('mode','value'),
             Input('deleteButton', 'n_clicks'),
             ],
         [
          State('scenarioname', 'value'),   
          State('conversionRate', 'value'),
          State('totalHits', 'value'),
          State('revenuePerPurchase', 'value'),
          State('ntpcuy','value'),
          State('samplingCost', 'value'),
          State('potentialRevenue', 'value'),
          State('ddselectscenario', 'value'),
          ])
def savescenarios(n_clicks,mode,deleteButton,scenarioname, conversionRate, totalHits, revenuePerPurchase, 
                  ntpcuy, samplingCost, potentialRevenue,ddselectscenario):
   ctx = dash.callback_context
   if ctx.triggered:
       eventid = ctx.triggered[0]['prop_id'].split('.')[0]
       if eventid =="saveButton":
            if 1 not in mode:
                sql = "SELECT max(scenario_id) as scenario_id FROM scenario_names"
                df = querydatafromdatabase(sql,[],["scenario_id"])
            
                if not df['scenario_id'][0]:
                    scenario_id=1
                else:
                    scenario_id = int(df['scenario_id'][0])+1
                sqlinsert = '''INSERT INTO 
                scenario_names(scenario_id,scenario_name,totalhits, 
                               conversionrate, revenueperpurchase, 
                               npurchaseperyear, costofsampling, 
                               percentrevenue) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
                modifydatabase(sqlinsert, (scenario_id,scenarioname,totalHits,conversionRate,revenuePerPurchase,
                                          ntpcuy,samplingCost,potentialRevenue  ))
            else:
                sqlinsert = '''UPDATE scenario_names SET scenario_name= ?,totalhits= ?, 
                               conversionrate= ?, revenueperpurchase= ?, 
                               npurchaseperyear= ?, costofsampling= ?, 
                               percentrevenue = ? WHERE scenario_id = ?'''
                modifydatabase(sqlinsert, (scenarioname,totalHits,conversionRate,revenuePerPurchase,
                                          ntpcuy,samplingCost,potentialRevenue,ddselectscenario  ))           
       elif eventid =="deleteButton":
            sqlinsert = '''DELETE FROM scenario_names WHERE scenario_id = ?'''
            modifydatabase(sqlinsert, (ddselectscenario,))
       sql = "SELECT scenario_name, scenario_id FROM scenario_names"
       df = querydatafromdatabase(sql,[],["label","value"])
       return [df.to_dict('records'),df.to_dict('records')[0]['value']]
   else:
       sql = "SELECT scenario_name, scenario_id FROM scenario_names"
       df = querydatafromdatabase(sql,[],["label","value"])
       return [df.to_dict('records'),df.to_dict('records')[0]['value']]

@app.callback(
         [
          Output('scenarioname', 'value'),   
          Output('conversionRate', 'value'),
          Output('totalHits', 'value'),
          Output('revenuePerPurchase', 'value'),
          Output('ntpcuy','value'),
          Output('samplingCost', 'value'),
          Output('potentialRevenue', 'value')
          
          ],
         [
             Input('ddselectscenario', 'value')],
         [
          ])
def loadcenarios(ddselectscenario):
    if ddselectscenario:
        sql = "SELECT * FROM scenario_names WHERE scenario_id=?"
        df = querydatafromdatabase(sql,[ddselectscenario],["scenario_id","scenario_name",'totalhits',
                                           "conversionrate","revenueperpurchase","npurchaseperyear","costofsampling","percentrevenue"])
       
        scenario_name = df["scenario_name"][0]
        totalhits = df["totalhits"][0]
        conversionrate = df["conversionrate"][0]
        revenueperpurchase = df["revenueperpurchase"][0]
        npurchaseperyear = df["npurchaseperyear"][0]
        costofsampling = df["costofsampling"][0]
        percentrevenue = df["percentrevenue"][0]
        return [scenario_name,conversionrate,totalhits,revenueperpurchase,npurchaseperyear,costofsampling,percentrevenue ]
    else:
        raise PreventUpdate

def querydatafromdatabase(sql, values,dbcolumns):
    db = sqlite3.connect('scenarios.db')
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dbcolumns)
    db.close()
    return rows

def modifydatabase(sqlcommand, values):
    db = sqlite3.connect('scenarios.db')
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()

