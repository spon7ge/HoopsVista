class Supplier:
    def __init__(self):
        # The key is the API key for the-odds-api at https://the-odds-api.com/#get-access
        self.key = "18d788cee86462294d091bcd8b1f50c5"
        
        # The directory is the location of the projections.json file
        self.directory = "/Users/alexg/Downloads/projections.json"
        # self.directory = "c:/Users/alexg/Downloads/projections.json"
    def get_key(self):
        return self.key
    
    def get_directory(self):
        return self.directory