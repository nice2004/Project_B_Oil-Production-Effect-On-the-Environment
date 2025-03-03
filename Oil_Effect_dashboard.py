import pandas as pd
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the datasets
data_set1 = pd.read_csv('oil-production-by-country.csv')
data_set2 = pd.read_csv('annual-co2-oil.csv')

# Merge the datasets on 'Entity' and 'Code'
dataset_merged = pd.merge(data_set1, data_set2, on=['Entity', 'Code']).drop_duplicates()

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


continent_zoom = {
    'Africa': {'lon': 50, 'lat': 0, 'scale': 2},
    'Asia': {'lon': 100, 'lat': 30, 'scale': 2},
    'Europe': {'lon': 20, 'lat': 50, 'scale': 2},
    'North America': {'lon': -100, 'lat': 40, 'scale': 2},
    'South America': {'lon': -60, 'lat': -15, 'scale': 2},
    'Oceania': {'lon': 140, 'lat': -25, 'scale': 2},
    'World': {'lon': 0, 'lat': 0, 'scale': 1},
}
country_to_continent = {
    'United States': 'North America',
    'Canada': 'North America',
    'Brazil': 'South America',
    'Argentina': 'South America',
    'Germany': 'Europe',
    'France': 'Europe',
    'China': 'Asia',
    'India': 'Asia',
    'Australia': 'Oceania',
    'South Africa': 'Africa',
    # Add more countries as needed
}


def create_choropleth_map(select_continent):
    filtered_dataset = dataset_merged[dataset_merged['Entity'] == select_continent]
    if select_continent not in continent_zoom:
        return px.choropleth()
    if select_continent == 'World':
        filtered_dataset = dataset_merged
    else:
        countries_in_continent = [country for country, continent in country_to_continent.items() if
                                  continent == select_continent]
        filtered_dataset = dataset_merged[dataset_merged['Entity'].isin(countries_in_continent)]

    choropleth_map = px.choropleth(
        filtered_dataset, locations='Code', color='Annual CO₂ emissions from oil',
        hover_name='Entity', animation_frame='Year_x',
        title=f'CO₂ Emissions from Oil in {select_continent}',
        color_continuous_scale=['gray', 'yellow', 'green', 'blue', 'violet', 'indigo'],
        range_color=[0, filtered_dataset['Annual CO₂ emissions from oil'].max()],
        labels={'Annual CO₂ emissions from oil': 'CO₂ Emissions (t)'}
    )
    choropleth_map.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="Black",
        lonaxis_range=[continent_zoom[select_continent]['lon'] - 30 / continent_zoom[select_continent]['scale'],
                       continent_zoom[select_continent]['lon'] + 30 / continent_zoom[select_continent]['scale']],
        lataxis_range=[continent_zoom[select_continent]['lat'] - 20 / continent_zoom[select_continent]['scale'],
                       continent_zoom[select_continent]['lat'] + 20 / continent_zoom[select_continent]['scale']]
    )
    return choropleth_map


# Build the app layout
app.layout = html.Div([
    html.H1('CO₂ Emissions Influenced by Oil Production Dashboard'),
    dcc.Tabs([
        dcc.Tab(label='Line Chart', children=[
            dcc.Graph(id='line-chart'),
            html.Div([
                dcc.Checklist(
                    id='country-checklist',
                    options=[{'label': country, 'value': country} for country in dataset_merged['Entity'].unique()],
                    value=['United States'],  # Default to United States
                    labelStyle={'display': 'block'}
                ),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Annual CO₂ emissions from oil', 'value': 'Annual CO₂ emissions from oil'},
                        {'label': 'Oil production (TWh)', 'value': 'Oil production (TWh)'}
                    ],
                    value='Annual CO₂ emissions from oil'  # Default metric
                )
            ], style={'width': '20%', 'float': 'right'})
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
                      dcc.Graph(id='choropleth-map')])
        ])
    ])
])


# Set up callbacks
@app.callback(
    Output('line-chart', 'figure'),
    Input('country-checklist', 'value'),
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
