import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime
import pandas as pd
from nsepy import get_history
from datetime import datetime
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

nsdq = pd.read_csv('./data/sectoral_tickers.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format('['+tic+']',nsdq.loc[tic]['Company Name']), 'value':tic})

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Stock Ticker Dashboard',style={'paddingRight':'30px',
                                            'textAlign': 'center',
                                            'color': colors['text']}),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight':'30px','color': colors['text']}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['APOLLOTYRE'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
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
    ], style={'display':'inline-block','backgroundColor': colors['background']}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        # df = web.DataReader(tic,'iex',start,end)
        df = get_history(symbol=tic, start=start, end=end)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        df = df.drop("Symbol", axis=1)
        traces.append({'x':df.index, 'y': df.Close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices',
                   'plot_bgcolor': colors['background'],
                   'paper_bgcolor': colors['background'],
                   'font': {
                       'color': colors['text']
                   }
                   }
    }
    return fig

if __name__ == '__main__':
    app.run_server()
