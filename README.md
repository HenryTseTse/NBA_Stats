## API
https://sportsdata.io/developers/api-documentation/golf#/sports-data-feed

#### Title of Site and Link to the URL Deployed

#### Website Description
My website is made for golf users that want to keep track of their golf rounds and have in depth statistics of their golf game. There are forms that take in additional information when recording golf rounds to provide in depth statistics about your golf game to help you improve! There is also a golf blog that keeps up to date with the PGA Tour including world rankings, golf news, leaderboards and profile description of players

#### Features
I have implemented many types of forms for editing and adding rounds, logging in and out for the user. Many golf statistics are calculated by only a few extra implementation to the golf round forms in which I dynamically calculated different stats with little information. This shows a in depth and real look of your golf portfolio with little effort. Calculations are done for you to see different parts of your game. This is also great to place to keep track of your golf rounds and calculates your handicap

#### Standard Flow
- First webpage is a home page that welcome a user and tells the user about the webpage, showing different screenshots of the website and description of images
- You are able to either log in or sign up, and after that you will be redirected to the home page which shows your golf portfolio
- Now whether you are a new user or existing ones, stats will automatically be adjusted to the rounds you have added. If there are no rounds, all stats will be set to 0 until you add a round
- There is another tab that links to a golf news tab which includes a overview of the golf news on a page. If you want to dive into specific leaderboards, look at upcoming PGA schedules, world rankings and PGA tour profiles, there are seprate tabs to get to those specific information

#### Technology stack
- I used flask for the main part of the website creating routes, HTML pages, forms
- I use SQLAlchemy to help me grab and filter information from my DataBase
- I use WTForms to help me create all my forms for my webpage
- I use JS with the API to help fetch and create/display data on the webpage
- CSS and Bootstrap to style my webpages 