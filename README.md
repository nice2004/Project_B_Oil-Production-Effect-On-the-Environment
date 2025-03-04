# Project B__Oil Production impact on Carbon dioxide Gas Emissions in the World

***Names: Nice Teta Hirwa*** <br />
***Instructor: Professor Mike Ryu*** <br />
***Class: CS-150*** <br />


## Thesis Statement
Designed a dashboard to visually analyze the effect of oil(gas) production in the world and its impact on the environment in
form of carbon dioxide (co2) gas emissions

## Context of my data visualization
Oil production is globally considered as a factor that contributes to the global economy representing a significant portion of the world's GDP.
In numbers,  oil and gas industry generates annual revenues around $3.5 trillion, accounting for approximately 3% of global GDP. Such
a huge amount! In this assignment, my aim was to assess whether the world cares about the balance of
socioeconomic development sectors (oil production in this case) with the environment. Or if they only care about what is going in their pocket,
without considering the environment. I answer this question by creating a dashboard that presents the annual co2 emission from oil over time.

## Data I will be visualizing
I visualized the annual carbon dioxide emissions from oil over time starting from 1990 to 2023. 
I displayed it using a primary graph -choropleth map that shows the data for the whole continents, but as a user you 
insert each continent you want to explore further. The secondary graph is a line graph, so whenever a user clicks on a country
of interest on the map, the user is automatically directed to the line graph that represents the same data
but in a form of a line graph.

## Call to Action
This is a call to action that most countries deteriorate the environment just by being blinded by money(GDP) that is generated from socio-economic factors.
This has to change! And one of the ways, we can do this is to be aware of this issue and advocating for change through our voting decisions,
and other similar routes.


## Strategies employed from SWD
1.  Articulating my unique point of view of the project, and why I chose the topic
2. Specifically conveying what’s at stake
3. Displaying what is happening, what should be the audiences' response, and how the data is being displayed correctly

## Explaining the coding part of the project
This code of this project has 6 main parts:
1. ***Filtered the data set*** - In this section, I filtered the dataset by being processed and read by panda, and filtering out 
the data from 1990 to 2023.
2. ***Created line chart*** - I created a function that takes in selected countries as a parameter since the line chart was in charge of displaying
line graphs of a selected country from the map. In this section, I filtered the dataset by giving it its x and y, created the title of the line graph 
and checked whether particular countries are in the dataset. 
3. ***Created choropleth map*** - a lot of logic about the latitude, longitude, and the zoom in and out numbers are in this particular function.
In here, I created a function that creates a choropleth map with the animation frame of years on the y-axis, added in colors, titles, and 
processed a csv that maps countries to continents so that a choropleth map would even be a content if a user wants to navigate the data in
continents.
4. ***CSS styling*** - Added in all the css styles such as the position of the header , container, tabs_container, etc
5. ***App layout*** - Created tabs for the switch from the choropleth map to line graph, created the UI and UX interface such as tabs, and
dropdowns for the line graphs and for the map.
6. ***Callbacks***: Created app calls for updating the selected country, updating the country dropdown, updating line charts, 
and finally updating the choropleth map

And I finally called the main() function to run the code.


