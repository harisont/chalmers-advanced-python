import json, re

def build_tram_stops(jsonobject):
  raw_data = json.load(jsonobject)
  geo_locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
  return geo_locs



def build_tram_lines(file):
  txt = file.read()
  
  keys = [re.sub(":\n$", "", l) for l in re.findall(".+:\n", txt)]
  stop_lists = [re.findall(".+\S+(?=\s{2,}\d+:\d+)", s) for s in re.split("\n\n", txt)]
  time_lists = [list(map(int, re.findall("(?<=\d\d:)\d+", l))) for l in re.split("\n\n", txt)]  

  lines = dict(zip(keys, stop_lists))

  times = {}
  for (sl1, sl2) in zip(stop_lists, time_lists):
    for (s1, t1, i) in zip(sl1, sl2, range(len(sl1))): 
      for (s2, t2) in zip(sl1[i:], sl2[i:]):
        """ 
        This part is ugly and could surely be written better.
        It does however ensure that the times are updated symmetrically. 
        """
        t = t2 - t1
        if s1 not in times.keys():
          times[s1] = {s2: t}
        if s2 not in times.keys():
          times[s2] = {s1: t}
        if s2 not in times[s1].keys():
          times[s1][s2] = t
        if s1 not in times[s2].keys():
          times[s2][s1] = t

        if t < times[s1][s2] or t < times[s2][s1]:
          times[s1][s2] = t
          times[s2][s1] = t

  return lines, times



def build_tram_network(somefiles = ['../data/tramstops.json' ,'../data/tramlines.txt']):
  out = {}
  try:
    with open(somefiles[0], 'r') as jsonobject:
      stops = build_tram_stops(jsonobject)
  except FileNotFoundError:
    print(f"Data base file not found on relative path: {somefiles[0]}")
  
  try:
    with open(somefiles[1], 'r') as txtfile:
      lines, times = build_tram_lines(txtfile)
  except FileNotFoundError:
    print(f"Tramline file not found on relative path: {somefiles[1]}")

  try:
      with open("./tramnetwork.json", 'w') as f:
        out = {"stops": stops, "lines": lines, "times": times}
        f.write(json.dumps(out))
  except FileNotFoundError:
    print(f"File path not")
  except FileExistsError: 
    print("File exists")


""" Function will return a alphabetically sorted list of trams that pass a stop. """
def lines_via_stop(lines, stop):
  raise NotImplementedError


""" Function will return a alphabetically sorted list of trams that go from stop A to B. """
def lines_between_stops(somedicts, stop1, stop2):
  raise NotImplementedError


""" Function returns the time from `stop1` to `stop2` along the given `line`. 
This is obtained as the sum of all distances between adjacent stops. 
If the stops are not along the same line, an error message is printed. """
def time_between_stops(somedicts, line, stop1, stop2):
  raise NotImplementedError

"""
Will give distance from stop A and B using formula at: 
https://en.wikipedia.org/wiki/Geographical_distance#Spherical_Earth_projected_to_a_plane
"""
def distance_between_stops(somedicts, stop1, stop2):
  raise NotImplementedError


if __name__ == "__main__":
  build_tram_network()
