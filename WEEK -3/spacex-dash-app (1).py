# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create a Dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown for launch sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[
                {'label': site, 'value': site}
                for site in launch_sites
            ]
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        }
    ),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2 CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(selected_site):

    if selected_site == 'ALL':

        filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()

        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

    else:

        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {selected_site}'
        )

    return fig


# TASK 4 CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def get_scatter_chart(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Outcome'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()