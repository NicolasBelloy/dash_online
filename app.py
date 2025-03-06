import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

data_path = './data/performance_data.csv'

# Load data
df = pd.read_csv(data_path, delimiter=',')

# Prepare data for clientside callback
data_dict = df.to_dict('list')

# App layout
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    dcc.Store(id='scatter-data', data=data_dict)
])

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(data) {
        var ntmpi = data.ntmpi;
        var ntomp = data.ntomp;
        var performance = data.Performance;
        var gpuCount = data['GPU Count'];

        var trace = {
            x: ntmpi,
            y: ntomp,
            z: performance,
            mode: 'markers',
            marker: {
                size: 5,  // Set all markers to the same size
                color: gpuCount,
                colorbar: {
                    title: 'GPU Count',
                    tickvals: [1, 2, 3, 4],
                    ticktext: ['1', '2', '3', '4']
                }
            },
            type: 'scatter3d'
        };

        var layout = {
            title: 'Performance vs ntmpi and ntomp',
            scene: {
                xaxis: {
                    title: 'ntmpi',
                },
                yaxis: {
                    title: 'ntomp'
                },
                zaxis: {
                    title: 'Performance (ns/day)'
                }
            },
            width: 1200,
            height: 800
        };

        return {
            data: [trace],
            layout: layout
        };
    }
    """,
    Output('scatter-plot', 'figure'),
    [Input('scatter-data', 'data')]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
