import pandas as pd
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the datasets
data_set1 = pd.read_csv('oil-production-by-country.csv')
data_set2 = pd.read_csv('annual-co2-oil.csv')

# Merge the datasets on 'Entity' and 'Code'
dataset_merged = pd.merge(data_set1, data_set2, on=['Entity', 'Code']).drop_duplicates()
dataset_merged = dataset_merged[dataset_merged['Year_x'] >= 2010]

# Print the first few rows and the columns of the merged dataset
print(dataset_merged.head())
print(dataset_merged.columns)

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


def create_line_chart(selected_countries, selected_metric):
    filtered_dataset = dataset_merged[dataset_merged['Entity'].isin(selected_countries)]
    return px.line(filtered_dataset, x='Year_x', y=selected_metric,
                   color='Entity',
                   title=f'{selected_metric} Change Over Time Due to Oil Production',
                   labels={'Year_x': 'Year', selected_metric: f'{selected_metric} (t)', 'Entity': 'Country'})


# Example with a different zoom scale (try values between 1.0 and 2.0 for continents)


continent_df = pd.read_csv('country_to_continent.csv')
country_to_continent = dict(zip(continent_df['Country'], continent_df['Continent']))


def create_choropleth_map(select_continent):
    # Define bounding box (lon_range and lat_range) for each continent
    continent_zoom = {
        'Africa': {'lon_range': [-20, 50], 'lat_range': [-35, 37]},
        'Asia': {'lon_range': [60, 180], 'lat_range': [10, 80]},
        'Europe': {'lon_range': [-30, 40], 'lat_range': [35, 75]},
        'North America': {'lon_range': [-170, -60], 'lat_range': [10, 85]},
        'South America': {'lon_range': [-85, -35], 'lat_range': [-60, 15]},
        'Oceania': {'lon_range': [110, 180], 'lat_range': [-55, 5]},
        'World': {'lon_range': [-180, 180], 'lat_range': [-90, 90]},
    }

    # Filter data based on selected continent
    if select_continent == 'World':
        filtered_dataset = dataset_merged
    else:
        countries_in_continent = [country for country, continent in country_to_continent.items() if
                                  continent == select_continent]
        filtered_dataset = dataset_merged[dataset_merged['Entity'].isin(countries_in_continent)]

    # Create the choropleth map
    choropleth_map = px.choropleth(
        filtered_dataset,
        locations='Code',
        color='Annual CO₂ emissions from oil',
        hover_name='Entity',
        animation_frame='Year_x',
        title=f'CO₂ Emissions from Oil in {select_continent}',
        color_continuous_scale=px.colors.sequential.Blues,
        range_color=[0, filtered_dataset['Annual CO₂ emissions from oil'].max()],
        labels={'Annual CO₂ emissions from oil': 'CO₂ Emissions (t)'}
    )

    # Update the map's geography (zoom settings)
    choropleth_map.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="Gray",
        lonaxis_range=continent_zoom[select_continent]['lon_range'],
        lataxis_range=continent_zoom[select_continent]['lat_range']
    )

    return choropleth_map


# Build the app layout
app.layout = html.Div([
    html.H1('CO₂ Emissions Influenced by Oil Production Dashboard'),
    dcc.Tabs([
        dcc.Tab(label='Line Chart', children=[
            dcc.Graph(id='line-chart'),
            html.Div([
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': country, 'value': country} for country in dataset_merged['Entity'].unique()],
                    multi=True,
                    style={'width': '80%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '10px'},
                    value=['United States'],  # Default to United States

                ),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Annual CO₂ emissions from oil', 'value': 'Annual CO₂ emissions from oil'},
                        {'label': 'Oil production (TWh)', 'value': 'Oil production (TWh)'}
                    ],
                    value='Annual CO₂ emissions from oil',
                    style={'width': '60%', 'display': 'inline-block', 'margin-left': '10px'}# Default metric
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
        ]),
        dcc.Tab(label='Choropleth Map', children=[
            html.Div([dcc.Dropdown(id='continent-dropdown',
                                   options=[{'label': 'Africa', 'value': 'Africa'},
                                            {'label': 'Asia', 'value': 'Asia'},
                                            {'label': 'World', 'value': 'World'},
                                            {'label': 'Europe', 'value': 'Europe'},
                                            {'label': 'North America', 'value': 'North America'},
                                            {'label': 'South America', 'value': 'South America'},
                                            {'label': 'Oceania', 'value': 'Oceania'}],
                                   value='World',
                                   style={'width': '50%'}),
                      dcc.Graph(id='choropleth-map',
                                style={'height': '600px', 'width': '1000px'})])
        ])
    ])
])


# Set up callbacks
@app.callback(
    Output('line-chart', 'figure'),
    Input('country-dropdown', 'value'),
    Input('metric-dropdown', 'value')
)
def update_line_chart(selected_countries, selected_metric):
    return create_line_chart(selected_countries, selected_metric)


@app.callback(
    Output('choropleth-map', 'figure'),
    Input('continent-dropdown', 'value')
)
def update_choropleth_map(selected_continent):
    return create_choropleth_map(selected_continent)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
