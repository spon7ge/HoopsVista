from collections import defaultdict
from WNBAPropFinder.ODDS_WNBA_SCRAPER import ODDS_WNBA_SCRAPER
from WNBAPropFinder.PRIZEPICKS_WNBA_SCRAPER import PRIZEPICKS_WNBA_SCRAPER
from BookWeight import BookWeight
import json
import os
from datetime import datetime 

class WNBAPropFinder():
    
    def __init__(self):
        self.nba_data = ODDS_WNBA_SCRAPER()
        self.prizepicks_data = PRIZEPICKS_WNBA_SCRAPER().lines
        self.book_to_weight = BookWeight().getBookToWeight()
        self.private_books = BookWeight().getPrivateBooks()
        self.categories = []
        self.condense()
        self.getData()
        
    def condense(self):
        temp = set()
        for x in self.prizepicks_data: # (name, type, line, date)
            temp.add(x[1])
        self.categories = list(temp)
        self.points_map = self.data_condenser(self.nba_data.points)
        self.rebounds_map = self.data_condenser(self.nba_data.rebounds)
        self.assists_map = self.data_condenser(self.nba_data.assists)
        self.threes_map = self.data_condenser(self.nba_data.threes)
        self.blocks_map = self.data_condenser(self.nba_data.blocks)
        self.steals_map = self.data_condenser(self.nba_data.steals)
        self.pra_map = self.data_condenser(self.nba_data.pra)
        self.pr_map = self.data_condenser(self.nba_data.pr)
        self.pa_map = self.data_condenser(self.nba_data.pa)
        self.ra_map = self.data_condenser(self.nba_data.ra)
        

    def data_condenser(self, data):
        ans = defaultdict(list)
        for prop in data:
            key = (prop[0], prop[1], prop[2])
            ans[key].append((prop[3], prop[4]))
        return ans
        
    def getCategory(self, category):
        if category == "Points":
            return self.sieve("Points", self.getPropsAverage(self.points_map))
        elif category == "Rebounds":
            return self.sieve("Rebounds", self.getPropsAverage(self.rebounds_map))
        elif category == "Assists":
            return self.sieve("Assists", self.getPropsAverage(self.assists_map))
        elif category == "3-PT Made":
            return self.sieve("3-PT Made", self.getPropsAverage(self.threes_map))
        elif category == "Blocked Shots":
            return self.sieve("Blocked Shots", self.getPropsAverage(self.blocks_map))
        elif category == "Steals":
            return self.sieve("Steals", self.getPropsAverage(self.steals_map))
        elif category == "Pts+Rebs+Asts":
            return self.sieve("Pts+Rebs+Asts", self.getPropsAverage(self.pra_map))
        elif category == "Pts+Rebs":
            return self.sieve("Pts+Rebs", self.getPropsAverage(self.pr_map))
        elif category == "Pts+Asts":
            return self.sieve("Pts+Asts", self.getPropsAverage(self.pa_map))
        elif category == "Rebs+Asts":
            return self.sieve("Rebs+Asts", self.getPropsAverage(self.ra_map))
        else:
            pass

    
    def getPropsAverage(self, map):
        ans = []
        for key, data in map.items():
            ans.append((key[0], key[1], key[2], self.weightedAverage(data)))
        sorted_ans = sorted(ans, key=lambda x: x[3])
        return sorted_ans
    
    def weightedAverage(self, data):
        odds_times_weight = 0
        sum_of_weights = 0
        for odds, book in data:
            if book in self.book_to_weight:
                odds_times_weight += odds*self.book_to_weight[book]
                sum_of_weights += self.book_to_weight[book]
            else:
                odds_times_weight += odds
                sum_of_weights += 1
            if book not in self.book_to_weight and book not in self.private_books:
                print("Book not in BookWeight: "+book)
        return round(odds_times_weight/sum_of_weights)
    
    def sieve(self, category, map):
        ans = []
        hold = set()
        for x in self.prizepicks_data: # (name, type, line, date)
            name, type, line = x[0], x[1], x[2]
            if type == category:
                hold.add((name, line-0.5, "whole"))
                hold.add((name, line, "half"))
                hold.add((name, line+0.5, "whole"))
        for name, type, line, odds in map:
            if (name, line, "half") in hold and odds > -140 and odds < 140:
                ans.append((name, type, line, odds, "half"))
        return ans
        
    def getData(self):
        all_props = {}
        for category in self.categories:
            if category in {"Points", "Rebounds", "Assists", "3-PT Made", "Blocked Shots", "Steals", "Pts+Rebs+Asts", "Pts+Rebs", "Pts+Asts", "Rebs+Asts"}:
                props = self.getCategory(category)
                all_props[category] = [
                    {"name": prop[0], "type": prop[1], "line": prop[2], "odds": prop[3], "half": prop[4]}
                    for prop in props
                ]
        return all_props

    def save_to_json_wnba(self, filename='WNBA_props.json'):
        data = self.getData()
        # Use an absolute path to the json_folder
        json_folder = os.path.abspath(os.path.join('..','..','..','backend', 'projectAI', 'predictor', 'json_folder'))  # Absolute path
        os.makedirs(json_folder, exist_ok=True)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f'WNBA_props({current_date}).json'
        file_path = os.path.join(json_folder, filename)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {file_path}")
