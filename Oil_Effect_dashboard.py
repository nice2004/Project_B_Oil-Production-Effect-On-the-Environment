import pandas as pd
from dash import dcc, Dash, html
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

dataset = pd.read_csv('annual-co2-oil.csv')
# inside - boolean, outside -- checks
dataset = dataset[dataset['Year'] >= 1990]

app = Dash(__name__,
           external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])


# create a line chart
def create_line_chart(selected_countries):
    filtered_dataset = dataset[dataset['Entity'].isin(selected_countries)]
    return px.line(filtered_dataset, x='Year', y='Annual CO₂ emissions from oil',
                   color='Entity',
                   title=f'Co2 annual gas emissions from oil Over Time for {", ".join(selected_countries)}',
                   labels={'Year': 'Year', 'Entity': 'Country',
                           },
                   template='plotly_white'
                   )


continent_df = pd.read_csv('Countries-Continents.csv')
country_to_continent = dict(zip(continent_df['Country'], continent_df['Continent']))


def create_choropleth_map(select_continent):
    continent_zoom = {
        'Africa': {'lon_range': [-20, 50], 'lat_range': [-35, 37]},
        'Asia': {'lon_range': [60, 180], 'lat_range': [10, 80]},
        'Europe': {'lon_range': [-30, 40], 'lat_range': [35, 75]},
        'North America': {'lon_range': [-170, -60], 'lat_range': [10, 85]},
        'South America': {'lon_range': [-85, -35], 'lat_range': [-60, 15]},
        'Oceania': {'lon_range': [110, 180], 'lat_range': [-55, 5]},
        'World': {'lon_range': [-180, 180], 'lat_range': [-90, 90]},
    }
    if select_continent == 'World':
        filtered_dataset = dataset
    else:
        countries_in_continent = [country for country, continent in country_to_continent.items() if
                                  continent == select_continent]
        filtered_dataset = dataset[dataset['Entity'].isin(countries_in_continent)]

    choropleth_map = px.choropleth(
        filtered_dataset,
        locations='Code',
        color='Annual CO₂ emissions from oil',
        hover_name='Entity',
        animation_frame='Year',
        title=f'CO₂ Emissions from Oil in {select_continent} (Click a country to view its line graph)',
        color_continuous_scale=px.colors.sequential.Blues,
        range_color=[0, filtered_dataset['Annual CO₂ emissions from oil'].max()],
        labels={'Annual CO₂ emissions from oil': 'CO₂ Emissions (t)'},
        template='plotly_white'
    )
    choropleth_map.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="Gray",
        lonaxis_range=continent_zoom[select_continent]['lon_range'],
        lataxis_range=continent_zoom[select_continent]['lat_range']
    )

    return choropleth_map


# CSS for styling

app_css = """
   .container {
       max-width: 1200px;
       margin: 0 auto;
       padding: 20px;
   }


   .header {
       text-align: center;
       margin-bottom: 20px;
       padding-bottom: 15px;
       border-bottom: 1px solid #e0e0e0;
   }


   .tabs-container {
       box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
       border-radius: 8px;
       overflow: hidden;
   }


   .controls {
       background: #f9f9f9;
       padding: 15px;
       border-radius: 5px;
       margin-bottom: 15px;
       display: flex;
       align-items: center;
       justify-content: space-between;
   }


   .control-item {
       margin-right: 15px;
   }


   .control-label {
       font-weight: bold;
       margin-bottom: 5px;
   }


   .instruction-box {
       background-color: #e8f4f8;
       border-left: 4px solid #3498db;
       padding: 10px 15px;
       margin: 10px 0;
       border-radius: 0 5px 5px 0;
   }
"""

# The app layout
app.layout = html.Div([

    # App container
    html.Div([

        # Header
        html.Div([
            html.H1('CO₂ Emissions from Oil Analysis',
                    style={'color': '#2c3e50', 'margin-bottom': '5px', 'text-align': 'center'}),
            html.P('Clicking on a country in the map gives access to view its line graph',
                   style={'color': '#7f8c8d'})
        ], className='header'),

        # what shows when the app runs
        dcc.Store(id='selected-country-store', data='United States'),
        dcc.Store(id='selected-tab-store', data='map-tab'),

        html.Div([  # Wrapper for the Tabs
            dcc.Tabs([

                # Map Tab
                dcc.Tab(
                    label='Map View',
                    value='map-tab',
                    children=[

                        # Map controls
                        html.Div([
                            html.Div([
                                html.Div('Select Region:', className='control-label'),
                                dcc.Dropdown(
                                    id='continent-dropdown',
                                    options=[
                                        {'label': 'World', 'value': 'World'},
                                        {'label': 'Africa', 'value': 'Africa'},
                                        {'label': 'Asia', 'value': 'Asia'},
                                        {'label': 'Europe', 'value': 'Europe'},
                                        {'label': 'North America', 'value': 'North America'},
                                        {'label': 'South America', 'value': 'South America'},
                                        {'label': 'Oceania', 'value': 'Oceania'}
                                    ],
                                    value='World',
                                    style={'width': '300px'}
                                )
                            ], className='control-item'),

                            html.Div([
                                html.I()
                            ], className='instruction-box')
                        ], className='controls'),

                        # Map visualization
                        dcc.Graph(
                            id='choropleth-map',
                            style={'height': '700px'},
                            config={'displayModeBar': True}
                        )
                    ]
                ),

                # Line Graph Tab
                dcc.Tab(
                    label='Line Graph',
                    value='line-tab',
                    children=[

                        # Line chart controls
                        html.Div([
                            html.Div([
                                html.Div('Select Countries:', className='control-label'),
                                dcc.Dropdown(
                                    id='country-dropdown',
                                    options=[{'label': country, 'value': country} for country in
                                             dataset['Entity'].unique()],
                                    multi=True,
                                    value=['United States'],
                                    style={'width': '400px'}
                                )
                            ], className='control-item'),

                            # Line chart visualization
                            dcc.Graph(
                                id='line-chart',
                                style={'height': '600px'}
                            )
                        ], className='line-chart-container')

                    ]
                )
            ], id='main-tabs', value='map-tab')
        ], className='tabs-container')

    ], className='container')
])


@app.callback(
    [Output('selected-country-store', 'data'),
     Output('main-tabs', 'value')],
    [Input('choropleth-map', 'clickData')],
    [State('selected-country-store', 'data')]
)
def update_selected_country(click_data, current_country):
    # click_data exists, update the selected country and switch to the line chart tab
    if click_data:
        clicked_country = click_data['points'][0]['hovertext']
        return clicked_country, 'line-tab'
    # no click_data, maintain the current country and don't change tabs
    raise PreventUpdate


@app.callback(
    Output('country-dropdown', 'value'),
    [Input('selected-country-store', 'data')]
)
def update_country_dropdown(selected_country):
    return [selected_country]


@app.callback(
    Output('line-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_line_chart(selected_countries):
    if not selected_countries:
        selected_countries = ['United States']  # Default if nothing selected

    fig = create_line_chart(selected_countries)
    # Enhance the layout
    fig.update_layout(
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


# Callback to update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('continent-dropdown', 'value')]
)
def update_choropleth_map(selected_continent):
    fig = create_choropleth_map(selected_continent)
    # Enhance the layout
    fig.update_layout(
        height=460,
        margin=dict(l=50, r=50, t=50, b=50),
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
