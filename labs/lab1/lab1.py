import json, re, math, sys

def build_tram_stops(jsonobject):
  raw_data:dict = json.load(jsonobject)
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
    print(f"File path not found")
  except FileExistsError: 
    print("File exists")


""" Function will return an numerically sorted list of trams that pass a stop. """
def lines_via_stop(lines, stop):
  return sorted([l for l in lines.keys() if stop in lines[l]], key= lambda x: int(x))
  

""" Function will return an numerically sorted list of trams that go from stop A to B. """
def lines_between_stops(lines, stop1, stop2) -> list:
  ans = [l for l in lines_via_stop(lines, stop1) if l in lines_via_stop(lines, stop2)]
  return sorted(ans, key = lambda x: int(x))


""" Function returns the time from `stop1` to `stop2` along the given `line`. 
This is obtained as the sum of all distances between adjacent stops. 
If the stops are not along the same line, an error message is printed. """
def time_between_stops(lines: dict, times: dict, line: str, stop1: str, stop2: str) -> int:
  stops: list = lines[line]
  if stop1 not in stops:
    print(f"{stop1} not a stop along line: {line}")
  if stop2 not in stops:
    print(f"{stop2} not a stop along line: {line}")
  
  x = 0
  r1 = range(stops.index(stop1), stops.index(stop2))
  r2 = r1 + 1
  for (s1, s2) in zip(stops[r1], stops[r2]):
    x+= times[s1][s2]
    # Make an try/catch if this fails due to database errors? 
  
  return x


"""
Will give distance from stop A and B using formula at: 
https://en.wikipedia.org/wiki/Geographical_distance#Spherical_Earth_projected_to_a_plane
"""
def distance_between_stops(stops: dict, stop1, stop2) -> float: # tested against example online
  R =  6371.009  # km 
  x2rad = math.pi/180
  dist = 0
  
  try: 
    (lat1, lon1) = zip(**stops[stop1])
    (lat2, lon2) = zip(**stops[stop2])
  except KeyError: 
    print("Latitude and longitude of one stop not in database. ")
    return dist
  
  mlat = 0.5 * (lat1+lat2) * x2rad # mean latitude in rads
  dlat = (lat2-lat1) * x2rad # delta latitude in rads
  dlong = (lon2 - lon1) * x2rad # delta longitude in rads 
  
  try: 
    dist = R*math.sqrt(dlat**2 + (math.cos(mlat) * dlong)**2)
  except ValueError: 
    print(f"Could not calculate distance between stops {stop1, stop2}", end=" ")
    print(f"with coordinates {lat1, lon1, lat2, lon2}")

  return dist


def dialogue(jsonfile = "./tramnetwork.json") -> None:
  try:
    with open(jsonfile, 'r') as f:
      db = json.load(f)
  except FileNotFoundError:
    print("Restart program with argument --init to build database.")
  
  get_arg = lambda q, p: re.match(p, q) != None
  
  """
  Read input, split it into a list of words 
  Read from start of string and match against fixed prompts to decide action
  Extract line and stop from argument, check if they exist
  If yes: return answer
  Else: print "unkown arguments"
  """

  while True: 
    print("> ", end = "")
    s = re.split("\s+", input())
    q = " ".join(s)
    if(get_arg(q, "^\s*quit\s*$")):
      break
    elif(get_arg(q, "^\s*via")):
      print("via")
    elif(get_arg(q,"^\s*between")):
      print("between")
    elif(get_arg(q,"^\s*time\s+with")):
      print("time with")
    elif(get_arg(q, "^\s*distance\s+from")):
      print("distance from")
    else:
      print("sorry, try again")





if __name__ == "__main__":
  if sys.argv[1:] == ['init']:
    build_tram_network()
  else:
    dialogue()			
