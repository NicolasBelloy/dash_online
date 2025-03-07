import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px

# Initialize the Dash app with the Flatly theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

data_path = './data/performance_data_array.csv'

# Load data
df = pd.read_csv(data_path, delimiter=',')

# Prepare data for clientside callback
data_dict = df.to_dict('list')

# Navbar layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Performance Dashboard", className="ms-2"),
        ]
    ),
    color="primary",
    dark=True,
)

# Sidebar layout
sidebar = dbc.Col(
    [
        html.H2("Filters", className="display-8"),
        html.Hr(),
        html.Label('Filter by ntmpi:'),
        dcc.Checklist(
            id='ntmpi-filter',
            options=[{'label': str(i), 'value': i} for i in sorted(df['ntmpi'].unique())],
            value=[i for i in sorted(df['ntmpi'].unique())],
            inline=True,
            className="mt-3"
        ),
        html.Label('Filter by ntomp:'),
        dcc.Checklist(
            id='ntomp-filter',
            options=[{'label': str(i), 'value': i} for i in sorted(df['ntomp'].unique())],
            value=[i for i in sorted(df['ntomp'].unique())],
            inline=True,
            className="mt-3"
        ),
        html.Label('Filter by GPU Count:'),
        dcc.Checklist(
            id='gpu-count-filter',
            options=[{'label': str(i), 'value': i} for i in sorted(df['GPU Count'].unique())],
            value=[i for i in sorted(df['GPU Count'].unique())],
            inline=True,
            className="mt-3"
        ),
    ],
    width=3,
    style={"padding": "20px"}
)

# Main content layout
content = dbc.Col(
    [
        dcc.Graph(id='scatter-plot'),
        dcc.Store(id='scatter-data', data=data_dict)
    ],
    width=9
)

# App layout
app.layout = dbc.Container(
    [
        navbar,
        html.Div(style={"margin-top": "20px"}),  # Add space between the banner and the rest of the content
        dbc.Row(
            [
                sidebar,
                content
            ]
        )
    ],
    fluid=True
)

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(data, ntmpiFilter, ntompFilter, gpuCountFilter) {
        var ntmpi = data.ntmpi;
        var ntomp = data.ntomp;
        var performance = data.Performance;
        var gpuCount = data['GPU Count'];

        if (ntmpiFilter.length > 0) {
            ntmpi = ntmpi.filter((value, index) => ntmpiFilter.includes(value));
            ntomp = ntomp.filter((value, index) => ntmpiFilter.includes(data.ntmpi[index]));
            performance = performance.filter((value, index) => ntmpiFilter.includes(data.ntmpi[index]));
            gpuCount = gpuCount.filter((value, index) => ntmpiFilter.includes(data.ntmpi[index]));
        }

        if (ntompFilter.length > 0) {
            ntmpi = ntmpi.filter((value, index) => ntompFilter.includes(data.ntomp[index]));
            ntomp = ntomp.filter((value, index) => ntompFilter.includes(value));
            performance = performance.filter((value, index) => ntompFilter.includes(data.ntomp[index]));
            gpuCount = gpuCount.filter((value, index) => ntompFilter.includes(data.ntomp[index]));
        }

        if (gpuCountFilter.length > 0) {
            ntmpi = ntmpi.filter((value, index) => gpuCountFilter.includes(data['GPU Count'][index]));
            ntomp = ntomp.filter((value, index) => gpuCountFilter.includes(data['GPU Count'][index]));
            performance = performance.filter((value, index) => gpuCountFilter.includes(data['GPU Count'][index]));
            gpuCount = gpuCount.filter((value, index) => gpuCountFilter.includes(value));
        }

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
                    title: 'ntmpi'
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
    [Input('scatter-data', 'data'), Input('ntmpi-filter', 'value'), Input('ntomp-filter', 'value'), Input('gpu-count-filter', 'value')]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
