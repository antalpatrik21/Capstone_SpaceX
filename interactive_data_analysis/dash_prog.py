import wget
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
url2 =  "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"

data =  wget.download(url)
program =  wget.download(url2)

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
#max_payload = spacex_df['Payload Mass (kg)'].max()
#min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

# Create an app layout
min_value = 0
max_value = 10000
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                ],
                                value='ALL',
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
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                      2500: '2500',
                                      5000 : '5000',
                                      7500: '7500',
                                       10000: '10000'},
                                value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy(deep=True)
    if entered_site == 'ALL':
        fig = px.pie(data_frame=filtered_df, values='class', 
        names='Launch Site', 
        title='Total number of successful launches from all site')
        return fig
    else:
        filtered_df = spacex_df.copy(deep=True)
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site].value_counts('class').to_frame().reset_index()
        filtered_df.rename(columns={0:'counts'} ,inplace=True) 
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values='counts', 
        names='class', 
        title=f'Total number of successful launches from {entered_site} site')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value"))
def get_scatter_plot(entered_site, pay):
    [min_payload, max_payload] = pay
    filtered_df = spacex_df.copy(deep=True)
    if entered_site == 'ALL':
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)']> min_payload) & (filtered_df['Payload Mass (kg)']<max_payload)]
        fig = px.scatter(filtered_df,title ='Correlation between payload mass (kg) and success for all sites', x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig

    else:
        filtered_df = spacex_df.copy(deep=True)
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)']> min_payload) & (filtered_df['Payload Mass (kg)']<max_payload)]

        # return the outcomes piechart for a selected site
        fig = px.scatter(filtered_df, title =f'Correlation between payload mass (kg) and success for {entered_site} site', x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()