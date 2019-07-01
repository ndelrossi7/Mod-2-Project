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
        team as well as stats on how many wins and losses the team had in the 2011 season."""
        
        for team in self.dictionary:
            plt.bar(x = [0, 1], height = [self.dictionary[team]['points', 'lost'], 
                              self.dictionary[team]['points', 'won']], tick_label = ['Won', 'Lost'])
            plt.title(team)
            plt.xlabel('Outcomes')
            plt.ylabel('Number of games')
            plt.show()
            plt.close()
            

to_graph = BuildGraph(unstacked_dict)

# Instantiating our dictionary so that we can call the graph function from our BuildGraph class