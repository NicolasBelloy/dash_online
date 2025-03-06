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
    dcc.Dropdown(
        id='gpu-count-dropdown',
        options=[
            {'label': '1 GPU', 'value': 1},
            {'label': '2 GPUs', 'value': 2},
            {'label': '3 GPUs', 'value': 3},
            {'label': '4 GPUs', 'value': 4}
        ],
        value=1,  # Default value
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Store(id='scatter-data', data=data_dict)
])

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(selectedGpuCount, data) {
        var ntmpi = data.ntmpi;
        var ntomp = data.ntomp;
        var performance = data.Performance;
        var gpuCount = data['GPU Count'];

        var filteredData = {
            ntmpi: [],
            ntomp: [],
            performance: [],
            gpuCount: []
        };

        for (var i = 0; i < gpuCount.length; i++) {
            if (gpuCount[i] == selectedGpuCount) {
                filteredData.ntmpi.push(ntmpi[i]);
                filteredData.ntomp.push(ntomp[i]);
                filteredData.performance.push(performance[i]);
                filteredData.gpuCount.push(gpuCount[i]);
            }
        }

        var trace = {
            x: filteredData.ntmpi,
            y: filteredData.ntomp,
            z: filteredData.performance,
            mode: 'markers',
            marker: {
                size: filteredData.performance,
                color: filteredData.gpuCount,
                #colorscale: 'Viridis',
                #colorbar: {
                #    title: 'GPU Count',
                #    tickvals: [1, 2, 3, 4],
                #    ticktext: ['1', '2', '3', '4']
                #}
            },
            type: 'scatter3d'
        };

        var layout = {
            title: 'Performance vs ntmpi and ntomp',
            scene: {
                xaxis: {
                    title: 'ntmpi',
                    tickmode: 'array',
                    tickvals: [2, 3, 4],
                    ticktext: ['2', '3', '4']
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
    [Input('gpu-count-dropdown', 'value')],
    [Input('scatter-data', 'data')]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

