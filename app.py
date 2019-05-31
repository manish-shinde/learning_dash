import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
# import pandas as pd
from nsepy import get_history
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H3(children='Enter Symbol to graph: Eg.SBIN',style={'paddingRight':'30px',
                                                             'textAlign': 'center',
                                                            'color': colors['text']}),
    dcc.Input(id='input', value='', type='text',style={'display':'inline-block','height': '40px'}),
html.Div([
        html.H3('Select start and end dates:',style={'color': colors['text']}),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px','color': colors['text']}
        ),
    ], style={'display':'inline-block'}),
    html.Div(id='output-graph'),
])

@app.callback(Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'),
     Input('submit-button', 'n_clicks')],
    [State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_value(input_data,n_clicks,start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    df = get_history(symbol=input_data, start=start, end=end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df = df.drop("Symbol", axis=1)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
            ],
            'layout': {'title': input_data +' Closing Prices',
                       'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                                'color': colors['text']
                                }
                       }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
