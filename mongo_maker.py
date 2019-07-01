import pymongo

class Mongo_maker(object):
    
    def __init__(self):
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017')
        self.mydb = self.myclient['2011_season_stats']
        self.mycollection = self.mydb['2011_season_stats']
    
    def format_data(self, name, totalgoals, totalwins, bar_graph, rain_wins):
        data = {"team_name": name,
               "total_goals": totalgoals,
               "total_wins": totalwins,
               "win_loss_graph": bar_graph,
               "rain_wins": rain_wins}
        
        return data
    
    def insert_record(self, record):
        return self.mycollection.insert_one(data)