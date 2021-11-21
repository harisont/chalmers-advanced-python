import json, re


def build_tram_stops(jsonobject):
  raw_data = json.load(jsonobject)
  locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
  return locs



def build_tram_lines(lines):
  txt = f.read()
  
  keys = [re.sub(":\n$", "", l) for l in re.findall(".+:\n", txt)]
  stop_lists = [re.findall(".+\S+(?=\s{2,}\d+:\d+)", s) for s in re.split("\n\n", txt)]
  time_lists = [list(map(int, re.findall("(?<=\d\d:)\d+", l))) for l in re.split("\n\n", txt)]  

  lines = dict(zip(keys, stop_lists))

  travel_times = {}
  for (sl1, sl2) in zip(stop_lists, time_lists):
    for (s1, t1, i) in zip(sl1, sl2, range(len(sl1))): 
      for (s2, t2) in zip(sl1[i:], sl2[i:]):
        """ This part is ugly and could surely be written better."""
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



def build_tram_network(somefiles = ['../data/tramstops.json' ,'../data/tramlines.txt']):
  try:
    with open(somefiles[0], 'r') as jsonobject:
      build_tram_stops(jsonobject)
  except FileNotFoundError:
    print(f"Data base file not found on relative path: {somefiles[0]}")
  
  try:
    with open(somefiles[1], 'r') as txtfile:
      build_tram_lines(txtfile)
  except FileNotFoundError:
    print(f"Tramline file not found on relative path: {somefiles[1]}")


if __name__ == "__main__":
  build_tram_stops
