'''
The task is to write:
1. Three functions that build dictionaries, 
2. Four functions that extract information from them, 
3. A dialogue function that answers to queries. 
   The dialogue function should be divided into two parts to enable more accurate testing.'''

import json, re


def build_tram_stops(jsonobject = '../data/tramstops.json'):
    try:
      with open(jsonobject, 'r') as f:
        raw_data = json.load(f)
        locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
      return locs
    except FileNotFoundError:
      print(f"Data base file not found on relative path: {jsonobject}")


""" Parses a text file and returns a dictionary """
def parse_file(f):
  
  txt = f.read()
  
  keys = [re.sub(":\n$", "", l) for l in re.findall(".+:\n", txt)]
  stops = [re.findall(".+\S+(?=\s{2,}\d+:\d+)", s) for s in re.split("\n\n", txt)]
  times = [list(map(int, re.findall("(?<=\d\d:)\d+", l))) for l in re.split("\n\n", txt)]  

  lines = dict(zip(keys, stops))

  travel_times = {}
  for (l1, l2) in zip(stops, times):
    for (s1, t1, i) in zip(l1, l2, range(len(l1))): 
      for (s2, t2) in zip(l1[i:], l2[i:]):
        # print(s1, s2, abs(t2-t1)) 
        t = t2 - t1
        if s1 not in travel_times.keys():
          travel_times[s1] = {s2: t}
        if s2 not in travel_times.keys():
          travel_times[s2] = {s1: t}
        if s2 not in travel_times[s1].keys():
          travel_times[s1][s2] = t
        if s1 not in travel_times[s2].keys():
          travel_times[s2][s1] = t

        if t < travel_times[s1][s2] or t < travel_times[s2][s1]:
          travel_times[s1][s2] = t
          travel_times[s2][s1] = t

  return lines, travel_times

  


def build_tram_lines(lines = '../data/tramlines.txt'):
    try:
      with open(lines, 'r', encoding='utf8',) as f:
        parse_file(f)
    except FileNotFoundError:
      print(f"Tramline file not found on relative path: {lines}")

if __name__ == "__main__":
  build_tram_stops()
  build_tram_lines()
