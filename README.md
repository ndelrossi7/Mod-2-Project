# Mod 2 Project

In this project, we used soccer match data from the kaggle SQL database: https://www.kaggle.com/laudanum/footballdelphi. We specifically looked at the 2011 season to find the following:
  1. How many goals each team scored throughout the season
  2. How many wins each team had throughout the season (displayed through bar graphs)
  3. What percentage of the time it was raining when a team won (weather data from DarkSky on the days of the matches in Berlin, Germany). 
  
## Importing Packages

To start, we need to ensure that we have all the necessary pacakages imported:

```python
import os
import numpy
import PIL
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import requests
import json
import apikey as api
```

## Importing data from SQL database 

We then have to extract our data from our SQL database and convert to a Pandas dataframe so that we can more easily visualize and work with our data. We'll extract our data from the 2011 season. 

```python
conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute("""SELECT * FROM Matches WHERE Season = 2011""")
matches = pd.DataFrame(c.fetchall())
matches.columns = [x[0] for x in c.description]
```
## Creating classes to work with and visualize our data

We now want to create a couple of classes to create our summary statistics and visualize/store our graphs for future MongoDB storage. 
We created the following classes:
```python
class MatchInfo:
    
    def __init__(self, df):
        self.df = df
        
    def total_goals(self):
        
        """Takes in our dataframe in question and outputs a dataframe 
        with the total number of goals for each team."""
        pass
    
    def team_names(self):
        
        """Takes in our dataframe in question and 
        outputs a list of all our team names."""
        
        pass

    def total_won(self):
        
        """Takes in our dataframe in question and outputs a 
        dataframe of the total games won per team."""
        
        pass
    
    def total_lost(self):
        
        """Takes in our dataframe in question and outputs a 
        dataframe of the total games lost per team."""
        
        pass
    
    
match_info = MatchInfo(matches)```
