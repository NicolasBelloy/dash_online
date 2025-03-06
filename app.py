import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

data_path = './data/performance_data.csv'

# Sample data
df = pd.read_csv(data_path, delimiter=',')

# App layout
app.layout = html.Div([
    dcc.Graph(id='bar-chart'),
    dcc.Dropdown(
        id='chart-type-dropdown',
        options=[
            {'label': 'Grouped', 'value': 'group'},
            {'label': 'Stacked', 'value': 'stack'}
        ],
        value='group',  # Default value
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Store(id='bar-data', data={'categories': categories, 'values1': list(values1), 'values2': list(values2)})
])

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(chartType, data) {
        var categories = data.categories;
        var values1 = data.values1;
        var values2 = data.values2;

        var barmode = chartType === 'stack' ? 'stack' : 'group';

        return {
            'data': [
                {
                    'x': categories,
                    'y': values1,
                    'type': 'bar',
                    'name': 'Series 1'
                },
                {
                    'x': categories,
                    'y': values2,
                    'type': 'bar',
                    'name': 'Series 2'
                }
            ],
            'layout': {
                'title': `Bar Chart (${chartType === 'stack' ? 'Stacked' : 'Grouped'})`,
                'barmode': barmode
            }
        };
    }
    """,
    Output('bar-chart', 'figure'),
    [Input('chart-type-dropdown', 'value')],
    [Input('bar-data', 'data')]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
