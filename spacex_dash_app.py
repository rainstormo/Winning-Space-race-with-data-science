# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    # Include options for each launch site in spacex_df
                                    {'label': 'Vandenberg Air Force Base', 'value': 'VAFB'},
                                    {'label': 'Cape Canaveral Space Launch Complex 40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'Kennedy Space Center Historic Launch Complex 39A', 'value': 'KSC LC-39A'},
                                    {'label': 'Cape Canaveral Space Launch Complex 40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'Kennedy Space Center Historic Launch Complex 39A', 'value': 'KSC LC-39A'}
                                    ],
                                    value='ALL',  # Default value set to 'ALL'
                                    placeholder="Select a Launch Site here",
                                    searchable=True                                
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                            min=0, 
                                            max=10000, 
                                            step=1000, 
                                            marks={i: f'{i}' for i in range(0, 10001, 1000)},
                                            value=[0, 10000])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
                     title='Total Success Launches by All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class', names='class', 
                     title=f'Success and Failed Launches for {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter the dataframe based on the payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        # Use all data within the selected payload range
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         labels={'class': 'Launch Outcome'},
                         title='Payload vs. Launch Outcome for All Sites')
    else:
        # Further filter by the selected launch site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         labels={'class': 'Launch Outcome'},
                         title=f'Payload vs. Launch Outcome for {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
