from collections import defaultdict
from NFLPropFinder.ODDS_NFL_SCRAPER import ODDS_NFL_SCRAPER
from NFLPropFinder.PRIZEPICKS_NFL_SCRAPER import PRIZEPICKS_NFL_SCRAPER
from BookWeight import BookWeight
import json
import os

class NFLPropFinder():
    
    def __init__(self):
        self.nfl_data = ODDS_NFL_SCRAPER()
        self.prizepicks_data = PRIZEPICKS_NFL_SCRAPER().lines
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
        self.passing_map = self.data_condenser(self.nfl_data.passing)
        self.receiving_map = self.data_condenser(self.nfl_data.receiving)
        self.attd_map = self.data_condenser(self.nfl_data.attd)
        self.rushing_map = self.data_condenser(self.nfl_data.rushing)

    def data_condenser(self, data):
        ans = defaultdict(list)
        for prop in data:
            key = (prop[0], prop[1], prop[2])
            ans[key].append((prop[3], prop[4]))
        return ans
    
    def getCategory(self, category):
        if category == "Pass Yards":
            return self.sieve("Pass Yards", self.getPropsAverage(self.passing_map))
        elif category == "Receiving Yards":
            return self.sieve("Receiving Yards", self.getPropsAverage(self.receiving_map))
        elif category == "Rush+Rec TDs":
            return self.sieve("Rush+Rec TDs", self.getPropsAverage(self.attd_map))
        elif category == "Rush Yards":
            return self.sieve("Rush Yards", self.getPropsAverage(self.rushing_map))
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
# {"Pass Yards", "Receiving Yards", "Rush+Rec TDs", "Rush Yards"}
    def getData(self):
        all_props = {}
        for category in self.categories:
            if category in {"Pass Yards", "Receiving Yards", "Rush+Rec TDs", "Rush Yards"}:
                props = self.getCategory(category)
                all_props[category] = [
                    {"name": prop[0], "type": prop[1], "line": prop[2], "odds": prop[3], "half": prop[4]}
                    for prop in props
                ]
        return all_props

    def save_to_json(self, filename='nba_props.json'):
        data = self.getData()
        # Use an absolute path to the json_folder
        json_folder = os.path.abspath(os.path.join('..','..','..','backend', 'projectAI', 'predictor', 'json_folder'))
        os.makedirs(json_folder, exist_ok=True)  
        file_path = os.path.join(json_folder, filename)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {file_path}")


