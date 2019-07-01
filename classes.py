import os
import numpy
import PIL
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute("""SELECT * FROM Matches WHERE Season = 2011""")
matches = pd.DataFrame(c.fetchall())
matches.columns = [x[0] for x in c.description]

# After connecting to the cursor, we have imported the SQL data from the matches table, which after inspection had all of the information that we needed for our summary statistics and visualizations. We then stored all the match data into a dataframe


class MatchInfo:
    
    def __init__(self, df):
        self.df = df
        
    def total_goals(self):
        
        """Takes in our dataframe in question and outputs a dataframe 
        with the total number of goals for each team."""
        
        home_goals = self.df.groupby('HomeTeam').sum()[['FTHG']]
        away_goals = self.df.groupby('AwayTeam').sum()[['FTAG']]
        total = home_goals.join(away_goals, how = 'inner')
        total['totals'] = total.FTHG + total.FTAG
        total_goals = total[['totals']] 
        total_goals.reset_index(inplace = True)
        total_goals.columns = ['TeamName', 'total_goals_scored']
        return total_goals
    
    def team_names(self):
        
        """Takes in our dataframe in question and 
        outputs a list of all our team names."""
        
        return list(self.df['HomeTeam'].unique())

    def total_won(self):
        
        """Takes in our dataframe in question and outputs a 
        dataframe of the total games won per team."""
        
        self.df['home_won'] = self.df.FTR.apply(lambda x: 1 if x == 'H' else 0)
        self.df['away_won'] = self.df.FTR.apply(lambda x: 1 if x == 'A' else 0)
        home_won = self.df.groupby('HomeTeam').sum()[['home_won']]
        away_won = self.df.groupby('AwayTeam').sum()[['away_won']]
        total_won = home_won.join(away_won, how = 'inner')
        total_won['total_won'] = total_won.home_won + total_won.away_won
        total_won = total_won[['total_won']]
        total_won.reset_index(inplace = True)
        total_won.columns = ['TeamName', 'total_games_won']
        return total_won
    
    def total_lost(self):
        
        """Takes in our dataframe in question and outputs a 
        dataframe of the total games lost per team."""
        
        self.df['home_lost'] = self.df.FTR.apply(lambda x: 1 if x == 'A' else 0)
        self.df['away_lost'] = self.df.FTR.apply(lambda x: 1 if x == 'H' else 0)
        home_lost = self.df.groupby('HomeTeam').sum()[['home_lost']]
        away_lost = self.df.groupby('AwayTeam').sum()[['away_lost']]
        total_lost = home_lost.join(away_lost, how = 'inner')
        total_lost['total_lost'] = total_lost.home_lost + total_lost.away_lost
        total_lost = total_lost[['total_lost']]
        total_lost.reset_index(inplace = True)
        total_lost.columns = ['TeamName', 'total_games_lost']
        return total_lost
    
    
match_info = MatchInfo(matches)
# Instantiating the dataframe to use when calling functions from our class

lost = match_info.total_lost()
won = match_info.total_won()
won_lost = won.merge(lost, how = 'inner', on = 'TeamName')
lost['type'] = 'lost'
lost.rename(columns = {'total_games_lost': 'points'}, inplace = True)
won['type'] = 'won'
won.rename(columns = {'total_games_won': 'points'}, inplace = True)
concat = pd.concat([won, lost], axis = 0)
concat.sort_values(by = 'TeamName', inplace = True)
concat.set_index(['TeamName', 'type'], inplace = True)
unstacked = concat.unstack()
unstacked_dict = unstacked.to_dict('index')

# playing around with dataframes to eventually make a dictionary which can be called for looped graphs

class BuildGraph:
    
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def build_graph(self):
        
        """This function takes in a dictionary and outputs a graph for each 
        team as well as stats on how many wins and losses the team had in the 2011 season.
        """
        os.makedirs('Team_Graphs')
        for team in self.dictionary:
            plt.bar(x = [0, 1], height = [self.dictionary[team]['points', 'lost'], 
                              self.dictionary[team]['points', 'won']], tick_label = ['Won', 'Lost'])
            plt.title(team)
            plt.xlabel('Outcomes')
            plt.ylabel('Number of games')
            plt.savefig("Team_Graphs/{}.png".format(team))
            plt.close()
            

to_graph = BuildGraph(unstacked_dict)

figs = os.listdir('Team_Graphs')

fig_dictionary = {}
for fig in figs:
    img = PIL.Image.open('team_graphs/{}'.format(fig)). convert('L')
    array = numpy.array(img)
    fig_dictionary.update({fig: array})
    
# Class to scrape the weather for the 2011 season
# Berlin coords 52.52437,13.41053
#######======================check which api key to use before running==============##############
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import sqlite3
import apikey as api
conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute('''SELECT * FROM Matches WHERE season = 2011;''')
data = pd.DataFrame(c.fetchall())
data.columns = [x[0] for x in c.description]



class weather_prepare:
    def __init__(self,data):
        self.data = data

    # prepare date for use in dark sky api -> convert to unix time
    def prepare_dataframe_for_weather(self):
        
        data.set_index('Match_ID', inplace = True)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Unix_Date'] = (data['Date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

unix = weather_prepare(data)

unix.prepare_dataframe_for_weather()

dates = data['Unix_Date']

# dates = dates.values.tolist()

class weather_scrape:
    def __init__(self):
        self.url = 'https://api.darksky.net/forecast'
        self.key = api.API_Key4
        self.latitude = "52.5200"
        self.longitude = "13.4050"
        self.exclude = 'currently,flags,minutely,hourly,alerts'
        self.df = data
        self.dates = dates

    def api_call(self):
        weather_dict = {}
        for date in self.dates:
            good_url = "{}/{}/{},{},{}?exclude={}".format(self.url,self.key,self.latitude, self.longitude, date, self.exclude)   
            response = requests.get(good_url)
            print(response)
            weather_data = response.json()['daily']['data'][0]['icon']
            weather_dict.update({date: weather_data})
        return weather_dict

    
#     api_call = api_call(date)

#     def all_the_weather(self, dates):
#         weather_dict = {}
#         for date in dates:
#             weather_data = weather_scrape.api_call(date)
#             weather_dict.update({date: weather_data})
#         return weather_dict

weather_data = weather_scrape()

weather = weather_data.api_call()

def adding_weather_to_df(weather):
    wdf = pd.DataFrame(weather, index = ['weather'])
    wdf2 = pd.DataFrame.transpose(wdf)
    wdf2 = wdf2.reset_index()
    wdf2.rename(columns={'index': 'Unix_Date'}, inplace=True)
    dfw = pd.merge(data, wdf2, how = 'left', on = 'Unix_Date')
    return dfw

    
# Instantiating our dictionary so that we can call the graph function from our BuildGraph class

final = adding_weather_to_df(weather)
final['weather'] = final.weather.apply(lambda x: 1 if x == 'rain' else 0)
final['all_weather'] = final.weather.apply(lambda x: 1)

# We created 2 new columns: 1 that allows us to sum the number of times it rained and 1 that allows us to sum 
# the total number of games

home_rain = final.groupby('HomeTeam').sum()[['weather']]
home_all = final.groupby('HomeTeam').sum()[['all_weather']]
away_rain = final.groupby('AwayTeam').sum()[['weather']]
away_all = final.groupby('AwayTeam').sum()[['all_weather']]

# We then summed these values to find the proportion of days when it rained

total_rain = home_rain.weather + away_rain.weather
total_weather = home_all.all_weather +away_all.all_weather
avg_weather = total_rain/total_weather*100

# We found the average number of times it rained

total_wins = match_info.total_won()
total_goal = match_info.total_goals()
games = total_wins.merge(total_goal, how = 'inner', on = 'TeamName')
dw = pd.DataFrame(avg_weather)
dw.reset_index(inplace = True)
dw.rename(columns = {0: 'rain_percent'}, inplace = True)
FINAL = pd.concat([games, dw], axis = 1)
FINAL.drop('HomeTeam', axis = 1, inplace = True)

# We merged our dataframes so as to see all of our data together and provide for easier MongoDB insertion