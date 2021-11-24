import json, re, math, sys

def build_tram_stops(jsonobject):
  raw_data:dict = json.load(jsonobject)
  geo_locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
  return geo_locs


def build_tram_lines(file):
  txt = file.read()
  
  keys = [l for l in re.findall(".+(?=:\n)", txt)]
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
  return sorted([l for l in lines.keys() if stop in lines[l]], key = lambda x: int(x))
  

""" Function will return an numerically sorted list of trams that go from stop A to B. """
def lines_between_stops(lines, stop1, stop2) -> list:
  ans = [l for l in lines_via_stop(lines, stop1) if l in lines_via_stop(lines, stop2)]
  return sorted(ans, key = lambda x: int(x))


""" Function returns the time from `stop1` to `stop2` along the given `line`. 
This is obtained as the sum of all distances between adjacent stops. 
If the stops are not along the same line, an error message is printed. """
def time_between_stops(lines: dict, times: dict, line: str, stop1: str, stop2: str) -> str:
  if line not in lines.keys():
    return f"line {line} not in database"
  
  stops: list = lines[line]
  
  if stop1 not in stops:
    return f"{line} does not stop at {stop1}"
  if stop2 not in stops:
    return f"{line} does not stop at {stop2}"
  
  return str(times[stop1][stop2])


"""
Will give distance from stop A and B using formula at: 
https://en.wikipedia.org/wiki/Geographical_distance#Spherical_Earth_projected_to_a_plane
"""
def distance_between_stops(stops: dict, stop1: str, stop2: str) -> float: # tested against example online
  R =  6371.009  # km 
  x2rad = math.pi/180
  dist = 0
  try: 
    (lat1, lon1) = map(float, (stops[stop1]['lat'], stops[stop1]['long']))
    (lat2, lon2) = map(float, (stops[stop2]['lat'], stops[stop2]['long']))
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

  while True: 
    print("> ", end = "")
    q = input()
    if(re.match("^\s*quit\s*$", q) != None):
      break
    else: 
      print( answer_query(db, q) )

def answer_query(tramdict, q: str):
  q = q.lower()
  args = "^\s*(via|between|time\swith|distance\sfrom)\s*"
  
  bad_args = "Unknown arguments."

  arg = ""
  if re.search(args, q) != None: 
    arg = re.search(args, q).group(0).strip()
  
  if arg == "via":
    stop = re.search("(?<=via).*", q)
    if stop != None:
      stop = re.search("(?<=via).*", q).group(0).strip().title()
      ans = lines_via_stop(tramdict["lines"], stop)
      if ans:
        return ", ".join(ans) 
      else:
        return bad_args
        # print(f"stop: {stop}. not found in database")
    
  elif arg == "between":
    if re.search("(?<=between).+\sand\s.+", q) != None:
      stop1 = re.search("(?<=between).+(?=\sand)", q).group(0).strip().title()
      stop2 = re.search("(?<=and\s).+", q).group(0).strip().title()
      ans = lines_between_stops(tramdict["lines"], stop1, stop2)
      if ans:
        return ", ".join(ans)
      else:
        return bad_args
    else: 
      return bad_args

  elif arg == "time with":
    args = re.search("(?<=time\swith)\s.+\sfrom\s.+\sto\s.+", q)
    if args != None:
      line = re.search("(?<=time\swith).+(?=\sfrom)", q).group(0).strip().title()
      stop1 = re.search("(?<=from\s).+(?=\sto)", q).group(0).strip().title()
      stop2 = re.search("(?<=to\s).+$", q).group(0).strip().title()
      
      if line not in tramdict["lines"].keys():
        return bad_args
      elif (stop1 or stop2) not in tramdict["stops"]:
        return bad_args
      else: 
        return time_between_stops(tramdict["lines"], tramdict["times"], line, stop1, stop2)
    else: 
      return bad_args
  
  elif arg == "distance from":
    args = re.search("(?<=distance from)\s.+\sto\s.+", q)
    if args != None:
      stop1 = re.search("(?<=from\s).+(?=\sto)", q).group(0).strip().title()
      stop2 = re.search("(?<=to\s).+$", q).group(0).strip().title()
    else:
      return bad_args

  else: 
    return "Sorry, try again."


if __name__ == "__main__":
  if sys.argv[1:] == ['init']:
    build_tram_network()
  else:
    dialogue()			
