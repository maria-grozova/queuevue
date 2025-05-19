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
- [Project learnings](#project-learnings)
  - [Data source](#data-source)
  - [Land field](#land-field)
  - [Dependencies for Streamlit deployment](#dependencies-for-streamlit-deployment)
  - [Further considerations](#further-considerations)
- [Testing](#testing)
  - [Manual testing](#manual-testing)
  - [Automated testing](#automated-testing)
- [App](#app)
  - [Live link](#live-link)
  - [Local setup](#local-setup)
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
<a href="Schema design"><img src="/readme_media/schema.png" align="right" width="20%" ></a> 
The initial schema design was intended to be a single CSV file, however due to encountering challenges over the time of the project this was adapted to 5 separate files using filtered views of the dataframe to calculate additional fields. The schema would be reviewed for v.2, given continuous development of the project. The chart shows the cleaned dataframe on the left and the final enriched output files on the right.

### Design choices
<a href="Windows 95"><img src="/readme_media/windows_95.png" align="right" width="20%" ></a> 
<a href="WebAim Screenshot"><img src="/readme_media/colour_contrast_check.png" align="right" width="20%" ></a> 
I have always been a fan of theme parks and used to spend many hours playing RollerCoaster Tycoon on the family PC. While I continue to be a fan of visiting theme parks as an adult, there is a special place in my heart for the design aesthetic of the 1999 game and Windows 95 OS it used to run on. I chose to evoke the classic Windows 95 colour scheme in the QueueVue web app, adjusting the original background colour #2B8282 to a lighter #00ABAD to ensure colour contrast accessibility adherence with the use of black font.

## Features
### Existing features
- **Home page**\
Clean but informative landing page explaining the purpose of the app, reference to the data source and an animation for some visual interest
********
- **Sidebar**\
Simple navigation sidebar that can be toggled in or out, with CTA and a list of pages
********
- **Theme park locations map**\
This shows the location of each theme park in the dataset as a marker on a map
********
- **Count of theme parks by continent**\
Metrics showing the number of theme parks in each continent
********
- **Bar chart showing the number of theme parks by country**\
The chart displays how many theme parks are in each country, colour coded by continent. This allows users to gauge theme park popularity in different areas
********
- **Selector to filter the wait times page by continent**\
The selector lets users filter the page results by continent. This is a single-select filter, default value is Europe
********
- **Bar chart showing the average wait time by ride, grouped by theme park**\
The chart shows the average wait time for each ride, grouped by theme park. This helps demonstrate the most popular rides in each park. The data is filtered by continent (user input). It is worth noting that some rides and parks have an average wait time of 0 minutes, in which case the chart won't display visuals
********
- **Metric displaying the longest recorded wait time**\
This shows the longest recorded wait time in the region (continent - user input), as well as the ride name, theme park, country and date the wait time was recorded. It's an interesting metric to see and can be surprising how long people are willing to wait for their or their kids' favourite rides!
********

### Planned features
- **Live wait times page**\
As the API data updates every 5 minutes, it would be interesting to set up a page that displays live wait times data and a comparison of live data to the historical gathered stats
- **Dataset growth**\
With the addition of regular data updates, the size of the dataset would eventually outgrow the current solution (selected for the restraints of the original brief). Here is an outline of how this would potentially change over time, based on my research
*********
**Phase 1 (Now to ~100MB)**
- Pre-calculate everything
- Save as 5 CSV files

**Phase 2 (~100MB to ~1GB)**\
Switch to incremental ETL:
- Daily ETL job appends new rows to a daily partitioned format, change to parquet from CSV as dataset grows for optimisation (/data/yyyy-mm-dd.parquet)
- Use AWS Glue Jobs (Python shell or Spark) or AWS Lambda for lightweight daily ETL, store in S3
- Use Amazon Athena to query Parquet files in S3 directly using SQL, which is serverless and cost-efficient for ad hoc querying

In Streamlit:
- Use @st.cache_data to load once and filter in memory (something I haven't explored yet at this point but could be implemented from the start on a future project)
- Use boto3 to fetch only relevant Parquet files from S3 (e.g., last 30 days or only the rows needed for a filter)

**Phase 3 (If growing beyond 1GB+)**\
- Use Amazon RDS for a managed PostgreSQL instance
- Store raw + processed data

In Streamlit:
- Use psycopg2 or SQLAlchemy to connect to RDS
- Query only the required subset and cache using @st.cache_data

*********
## Project learnings
This being my first end-to-end ETL project, I encountered a number of challenges which resulted in a lot of learnings for future work.
### Data source
Up until this project I had mostly used CSV files for practicing Pandas and Streamlit. Having a nested JSON presented a number of challenges I hadn't immediately picked up on. Firstly, due to the structure I had to write a function that would normalise the JSON before I am able to convert it into a Pandas dataframe. By initially testing it on a small number of park id's I missed the inconsistencies between different records where the ride entities are either nested within the land array or are up a level in the rides array. I made a diagram that helped me understand and fix this, however this meant my initial dataset fetched over multiple days was unusable. This was a good learning curve, but it did eat into my project time and I likely would've had a lot more success with a CSV or a flat JSON for my first end to end project.
![JSON structure](/readme_media/json_structure_diagram.png)
### Land field
Further inconsistencies in the data source - the 'land' field either describes the type of ride, the name of the land the ride is located in, or null. This was difficult to spot early on as I didn't have experience telling me that's something to look out for. I intended originally to incorporate grouping by ride types in the data analysis, however the discovery of the inconsistencies quite late in the project meant I had to drop this field. It wasn't usable without significant cleaning and transformation, but in the future I will know to look out for this type of issue and potentially seek an alternative data source in a similar situation.
### Dependencies for Streamlit deployment
During deployment, I encountered a dependency error caused by the psycopg2 package, which I resolved by switching to psycopg2-binary in the requirements.txt file. Additionally, I had to update the Streamlit version to enable the filter component I was using. After addressing these issues, the deployment completed successfully.
### Further considerations
I’ve included try-except blocks in the code to catch and handle potential errors. These blocks print messages indicating success or failure, which helps with debugging and improves code reliability. In the future, this could be enhanced by logging errors to a file or monitoring system for better tracking and analysis.\
Currently, there are no security or privacy concerns since the dataset used is public. To future-proof the code, I would implement input validation, secure file handling, and consider anonymizing or encrypting sensitive data if private datasets are used in later iterations
## Testing
### Manual testing
Manual testing of the outputs has been completed utilisting Jupyter notebooks. This involved running various test cases, inspecting the intermediate results, and validating the final outputs against expected values. The interactive environment of Jupyter allowed for step-by-step execution and easy debugging, ensuring the core functionalities perform as intended
### Automated testing
The automated pytest shows that all tests pass successfully, but the code coverage is below the required threshold of 90% (currently at 82%). I would look to improve the tests coverage in v.2, however a lot of the functions already include try/except blocks that are helpful if debugging is required
## App
### Live link
[QueueVue app on Streamlit](https://queuevue.streamlit.app/)
### Local setup
- Fork and clone the repo
- Install and activate a virtual environment
- Run command in terminal *pip install -r requirements-setup.txt*
- Run command in terminal *pip install -e .*
- To run ETL *run_etl {dev/test}*
- To run tests *run_tests all*
- To run Streamlit locally *streamlit run Home.py*

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
