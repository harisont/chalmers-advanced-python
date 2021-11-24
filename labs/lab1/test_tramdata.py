import unittest
# from tramdata import *
import json, re
from lab1 import *
# from hypothesis.strategies import text
from math import acos, cos, sin, radians
TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict: dict = tramdict['stops']
            self.linedict: dict = tramdict['lines']
            self.timedict: dict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here

    """ Tests that all distances are reasonable, i.e. < 20 km. """
    def test_max_range(self, max_dist=20):
        print("")
        dist_list = []
        for A in self.stopdict.keys():
            for B in self.stopdict.keys():
                d = distance_between_stops(self.stopdict, A, B)  # do we need to verify this function? 
                if d > max_dist:
                    print(f"FAILED with dist {d} > {max_dist} between stops {A, B}", end = "\n\n")
                    return 
        print(f"OK: distances < {max_dist}")
        print("")

    """ Tests that all the keys found in the text file are also in the database """
    def test_lines_exists(self):
        with open("../data/tramlines.txt") as f:
            
            keys_list = set(re.findall(".+(?=:\n)", f.read()))

            if self.linedict.keys() != keys_list: 
                print("FAILED: test lines exists")

    def test_line_stops_exist(self):
        with open("../data/tramlines.txt") as f:
            key = ""
            stop = ""
            for row in f.readlines():
                is_key = re.search(".+(?=:\n)", row)
                is_stop = re.search(".+(?=\s+\d\d:\d\d\n)", row)

                if is_key:
                    key = is_key.group(0).strip()
                    if key not in self.linedict.keys():
                        print(f"FAILED: line: {key} not in database with lines: {self.linedict.keys()}")
                        return
                elif is_stop:
                    stop = is_stop.group(0).strip()
                    if stop not in self.linedict[key]:
                        print(f"FAILED: stop: {stop} not in database for line {key} with stops: {self.linedict.values()}")
                        return                    
        print("OK: all line and stops in database. ")






if __name__ == '__main__':
    unittest.main()

