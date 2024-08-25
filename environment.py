import random
import time

class Env:
    def __init__(self):
        
        self.zones = [
                {"id": 'A1', "probability": 0.5},
                {"id": 'A2', "probability": 0.25},
                {"id": 'A3', "probability": 0.05},
                {"id": 'B1', "probability": 0.0},
                {"id": 'B2', "probability": 0.1},
                {"id": 'B3', "probability": 0.1}
                ]
        
    def generate_food(self):
        for zone in self.zones:
            zone["food"] = random.random() <= zone["probability"]
        time.sleep(0.2)
        print("--------------------------------------------")
        
    
    def get_zones(self):
        return self.zones
