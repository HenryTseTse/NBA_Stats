## NBA Stats
https://nba-stats-tvb5.onrender.com/

### Description
NBA Stats is used for basketball fans to follow along with today's game as well as learn the history of the game. Statistics are a big part of basketball as box scores is a convenient way to see how their favorite teams and players are performing. Fans can access and learn about different teams, as they can even quickly gain access to information straight from the Offical NBA Website. 

### Features

Users can quickly access the top 5 leaders in each statistical category right on the homepage. There are dropdown buttons to quickly toggle players for major categories with headshots for each player. This allows the user to be more integrated with the application as stats are updated close-to-date depending on when the data was last scraped.

Once registered, users can access multiple forms to view various team and player stats. There are additional forms that allow fans to search through player historical stats and certain games where players hit a certain threshold. The **Teams** tab gives information to the user about the abbreviation for each team and also allows the user to quickly access each teams' offical NBA homepage. Using the abbreviations provided from the teams tab, the **H2H** feature allows the user to filter through each team and view detailed stats for the provided season.

Users also have access to player stats. Through the **Player Search** feature, users provide a first and last name that will be used to generate season career stats along with a headshot of the player. In addition, the **Advanced Search** options give users the ability to view detailed game stats in which a timeframe and optional thresholds for certain stats are provided.

### API
- API: https://www.balldontlie.io/home.html#introduction
- Image Src: https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png

There was no free alternative option to easily provide player headshots. I noticed a pattern from the official NBA website in how they sourced their images. Each image had a given link and a NBAID used for each player. I data scrapped NBAIDs for each player and stored them into a database to quickly access each image.

### Technology Stack
- Python was the main programming language used for this web application to populate our database and implement Back-end and Front-end technologies
- Flask was the main component for creating routes, HTML pages, and forms
- SQLAlchemy was used to retrieve and filter information from the database
- WTForms was used to create forms for the application
- Javascript was used along with AJAX to create the toggle feature to asynchronously display "Top 5" without interfering with the display and behavior of the existing page
- CSS and Bootstrap was used to style the website

### Developer Notes
- Create Virtual Environment: python -m venv venv (ENV Version: Python 3.7.10)
- Activate Virtual Environment: source venv/bin/activate
- Install Dependancies: pip install requirements.txt
- Preload Database: python scripts/seed.py, python scripts/top5.py