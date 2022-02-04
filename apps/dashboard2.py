import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

# Add dashboard specific methods here

def get_dashboard2_layout():

    # Call dashboard specific methods here

    return [
        html.Div(children='Incorrect Username/Password',style={'padding-left':'540px','padding-top':'40px','font-size':'16px', 'color':'#FF0000', 'font':'verdana'})
    ]
