# QueueVue
### Theme park queue times analysis.
Digital Futures DE12 Capstone Project - ETL and Streamlit

![RollerCoaster Tycoon gif](/readme_media/rollercoaster_tycoon.gif)

## Contents
- [UX and Design](#ux-and-design)
  - [Site goals](#site-goals)
  - [Direction](#direction)
  - [User stories](#user-stories)
  - [Schema design](#schema-design)
  - [Design choices](#design-choices)
- [Features](#features)
  - [Existing features](#existing-features)
  - [Planned features](#planned-features)
- [Testing](#testing)
  - [Manual testing](#manual-testing)
  - [Validator testing](#validator-testing)
- [Deployment](#deployment)
  - [Live link](#live-link)
- [Resources and credits](#resources-and-credits)
  - [Data](#data)
  - [Media](#media)
  - [Code](#code)

## UX and Design
### Site goals
Our web app will let users explore data analysis based on the wait times data for global theme parks which will affect theme park and data enthusiasts by being able to learn some interesting trends, facts and enjoy a visual representation of this data.

### Direction
The principles and needs that were considered.

How might we:
- make it intuitive for users to explore the analysis of queue times and trends
- make it easy to understand the site's theme and purpose
- ensure the data displayed is clean and factual

### User stories
I identified 5 user user stories for the MVP.
The project progress was planned and tracked using Agile, as documented here in [GitHub Project](https://github.com/users/maria-grozova/projects/7)

### Schema design
The initial schema design was intended to be a single CSV file, however due to encountering challenges over the time of the project this was adapted to 5 separate files using filtered views of the dataframe to calculate additional fields. The schema would be reviewed for v.2, given continuous development of the project. The chart shows the cleaned dataframe on the left and the final enriched output files on the right.
*******

### Design choices
<a href="Windows 95"><img src="/readme_media/windows_95.png" align="right" width="20%" ></a> 
<a href="WebAim Screenshot"><img src="/readme_media/colour_contrast_check.png" align="right" width="20%" ></a> 
I have always been a fan of theme parks and used to spend many hours playing RollerCoaster Tycoon on the family PC. While I continue to be a fan of visiting theme parks as an adult, there is a special place in my heart for the design aesthetic of the 1999 game and Windows 95 OS it used to run on. I chose to evoke the classic Windows 95 colour scheme in the QueueVue web app, adjusting the original background colour #2B8282 to a lighter #00ABAD to ensure colour contrast accessibility adherence with the use of black font.

## Features
### Existing features
- Home page
******
Clean but informative landing page explaining the purpose of the app, reference to the data source and an animation for some visual interest
- Sidebar
******
Simple navigation sidebar that can be toggled in or out, with CTA and a list of pages
- Theme park locations map
********
This shows the location of each theme park in the dataset as a marker on a map
- Counter of theme parks by continent
********
Metrics showing the number of theme parks in each continent
- Bar chart showing the number of theme parks by country
********
The chart displays how many theme parks are in each country, colour coded by continent. This allows users to gauge theme park popularity in different areas.
- Selector to filter the wait times page by continent
********
The selector lets users filter the page results by continent. This is a single-select filter, default value is Europe
- Bar chart showing the average wait time by ride, grouped by theme park
********
The chart shows the average wait time for each ride, grouped by theme park. The data is filtered by continent (user input). It is worth noting that some rides and parks have an average wait time of 0 minutes, in which case the chart won't display visuals
- Metric displaying the longest recorded wait time
********
This shows the longest recorded wait time in the region (continent - user input), as well as the ride name, theme park, country and date the wait time was recorded

### Planned features
- Live wait times page
## Project learnings
This being my first end-to-end ETL project, I encountered a number of challenges which resulted in a lot of learnings for future work.
### Data source
Nested JSON bad
![JSON structure](/readme_media/json_structure_diagram.png)
## Testing
### Manual testing
- ***

### Validator testing
- ***

## Deployment
- ***

### Live link
***

## Resources and credits
### Data
- The data in this project, including the parks' metadata, ride names, locations and wait times is fetched from [Queue Times API](https://queue-times.com/)

### Media
- Home page animation from [Lottie Animation](https://lottiefiles.com/free-animation/roller-coaster-sA1NACEeoj), licensed under FL 9.13.21.
- Gif used in the ReadMe file is from [Giphy](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExajNsMWFlNnFlcDZtdzNlZzRpOHNiNXF1M3RmYW9uajh5eDVrYXdwMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Gt0j4zPgzHL8pTPiqc/giphy.gif)
- Windows 95 screen for the ReadMe is from [Wikipedia](https://en.wikipedia.org/wiki/Windows_95)
- Colour contrast checker screenshot made using [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- JSON structure diagram and schema design made using [Lucidchart](https://www.lucidchart.com/)

### Code
- Code for the animation implementation on the home page was sourced from [Geeks For Geeks Article](https://www.geeksforgeeks.org/adding-lottie-animation-in-streamlit-webapp/)
- [Streamlit documentation](https://docs.streamlit.io/) for reference
- [Pandas documentation](https://pandas.pydata.org/docs/) for reference
- Digital Futures - [ETL Project Demo](https://github.com/de-2502-a/etl-project-demo/tree/initial-project-setup) was referenced for the initial commit of this project
- Special thank you to Hamza, Alex and Bassmah at Digital Futures for support and tips

