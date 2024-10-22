import os
from dotenv import load_dotenv

load_dotenv()

class Supplier:
    def __init__(self):
        # The key is the API key for the-odds-api at https://the-odds-api.com/#get-access
        self.key = os.getenv('api_key')
        
        # The directory is the location of the projections.json file
        # self.directory = "/Users/alexg/Downloads/projections.json"
        self.directory = "c:/Users/alexg/Downloads/projections.json"

    def get_key(self):
        return self.key
    
    def get_directory(self):
        return self.directory