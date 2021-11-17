'''
The task is to write:
1. Three functions that build dictionaries, 
2. Four functions that extract information from them, 
3. A dialogue function that answers to queries. 
   The dialogue function should be divided into two parts to enable more accurate testing.'''

import json, csv, re


def build_tram_stops(jsonobject = '../data/tramstops.json'):
    try:
      with open(jsonobject, 'r') as f:
        raw_data = json.load(f)
        locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
    except FileNotFoundError:
      print(f"Data base file not found on relative path: {jsonobject}")

def build_tram_lines(lines = '../data/tramlines.txt'):
    try:
      with open(lines, 'r', encoding='utf8',) as f:
          ls = f.read().split("\n\n")
          del ls[-1] # to deal with trailing \n\n
          
          for l in ls:
            print(l)
            # gets each tram line as a separate string object in the list ls.
          

    except FileNotFoundError:
      print(f"Tramline file not found on relative path: {lines}")

if __name__ == "__main__":
  build_tram_stops()
  build_tram_lines()
