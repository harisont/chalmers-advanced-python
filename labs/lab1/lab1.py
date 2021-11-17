import json
import csv 

def build_tram_stops(PATH = 'labs/data/tramstops.json'):
  try: 
    with open(PATH) as f:
      raw_data = json.load(f)
  except FileNotFoundError:
    print(f"Data base file not found on relative path: {PATH}")
  
  locs = {k : {'lat': v["position"][0] , 'long': v["position"][1]} for (k,v) in raw_data.items()}

def build_tram_lines(PATH = 'labs/data/tramlines.tsv'):    
  
  














if __name__ == "__main__":
  build_tram_stops()