# %% [markdown]
# # Formula 1 analysis 2023 vs 2024(upto Brazil GP)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## Bahrain GP

# %%
import fastf1
from fastf1 import plotting
import plotly.graph_objects as go
import os

fig=go.Figure() #create a figure object to plot the data
# Create cache directory if it does not exist
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

fastf1.Cache.enable_cache(cache_dir) #enable cache to store the data 
def get_lap_times(year, race, drivers=['HAM', 'RUS']):
    """Fetch lap times for a specific race and year for Mercedes drivers."""
    session = fastf1.get_session(year, race, 'R')  # Load Race session
    session.load(telemetry=False, weather=False, laps=True)  # Ensure laps data is loaded

    lap_times = {}
    for driver in drivers:
        driver_laps = session.laps.pick_driver(driver)
        lap_times[driver] = driver_laps['LapTime'].dt.total_seconds()  # Convert timedelta to seconds

    return lap_times

# Define the races to include up to Brazil GP
races = ['Bahrain', 'Saudi Arabia', 'Australia', 'Azerbaijan', 'Miami', 'Emilia Romagna', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'Hungary', 'Belgium', 'Netherlands', 'Italy', 'Singapore', 'Japan', 'United States', 'Mexico', 'Brazil']

# Initialize dictionaries to store lap times for all races
lap_times_2023_all = {}
lap_times_2024_all = {}

# Fetch lap times for each race and store them in the dictionaries
for race in races:
    lap_times_2023_all[race] = get_lap_times(2023, race)
    lap_times_2024_all[race] = get_lap_times(2024, race)

# Visualize lap times for each race
for race in races:
    fig = go.Figure()
    
    # Add data for 2023
    for driver, times in lap_times_2023_all[race].items():
        fig.add_trace(go.Scatter(x=list(range(1, len(times) + 1)), y=times, mode='lines+markers', name=f'{driver} - 2023'))

    # Add data for 2024
    for driver, times in lap_times_2024_all[race].items():
        fig.add_trace(go.Scatter(x=list(range(1, len(times) + 1)), y=times, mode='lines+markers', name=f'{driver} - 2024'))

    # Update layout
    fig.update_layout(
        title=f'Mercedes Lap Times: {race} GP (2023 vs 2024)',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        legend_title="Driver & Year",
        template='plotly_dark',  # Optional: for a dark-themed plot
        hovermode='closest'  # Interactive hover effect
    )

    # Show the plot
    fig.show()

# %%
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.io as pio

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Formula 1 Lap Times Analysis (2023 vs 2024)"),
    dcc.Dropdown(
        id='race-dropdown',
        options=[{'label': race, 'value': race} for race in races],
        value=races[0]
    ),
    dcc.Graph(id='lap-times-graph')
])

# Define the callback to update the graph based on selected race
@app.callback(
    Output('lap-times-graph', 'figure'),
    [Input('race-dropdown', 'value')]
)
def update_graph(selected_race):
    fig = go.Figure()
    
    # Add data for 2023
    for driver, times in lap_times_2023_all[selected_race].items():
        fig.add_trace(go.Scatter(x=list(range(1, len(times) + 1)), y=times, mode='lines+markers', name=f'{driver} - 2023'))

    # Add data for 2024
    for driver, times in lap_times_2024_all[selected_race].items():
        fig.add_trace(go.Scatter(x=list(range(1, len(times) + 1)), y=times, mode='lines+markers', name=f'{driver} - 2024'))

    # Update layout
    fig.update_layout(
        title=f'Mercedes Lap Times: {selected_race} GP (2023 vs 2024)',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        legend_title="Driver & Year",
        template='plotly_dark',  # Optional: for a dark-themed plot
        hovermode='closest'  # Interactive hover effect
    )

    # Save the dashboard to an HTML file
    pio.write_html(fig, file=os.path.expanduser('C:/Users/sanat/Documents/f1_lap_times_dashboard.html'), auto_open=False)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get('PORT', 8050)), host='0.0.0.0') #run the app in the Jupyter notebook

# %%


# %%



