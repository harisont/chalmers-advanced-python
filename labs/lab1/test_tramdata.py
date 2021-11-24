import unittest
from tramdata import *
import json, re
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
                msg = f"FAILED with dist {d} > {max_dist} between stops {A, B}"
                self.assertLess(d, max_dist, msg)
                    
        print(f"OK: distances < {max_dist}")

    """ Tests that all the keys found in the text file are also in the database """
    def test_lines_exists(self):
        with open("../data/tramlines.txt") as f:
            
            keys_list = set(re.findall(".+(?=:\n)", f.read()))
            msg = f"{keys_list.symmetric_difference(self.linedict.keys())}"
            self.assertEqual(keys_list, self.linedict.keys(), msg)

    def test_line_stops_exist(self):
        print("")
        with open("../data/tramlines.txt") as f:
            key = ""
            stop = ""
            for row in f.readlines():
                is_key = re.search(".+(?=:\n)", row)
                is_stop = re.search(".+(?=\s+\d+:\d+\n)", row)

                if is_key:
                    key = is_key.group(0).strip()
                    msg = f"FAILED: line: {key} not in database with lines: {self.linedict.keys()}"
                    self.assertIn(key, self.linedict.keys(), msg)
                elif is_stop:
                    stop = is_stop.group(0).strip()
                    msg = f"FAILED: stop: {stop} not in database for line {key} with stops: {self.linedict[key]}"
                    self.assertIn(stop, self.linedict[key], msg)
                        
        print("OK: all line and stops in database. ")

    def test_symmetric_travel_time(self):
        for line in self.linedict.keys():
            for s1 in self.linedict[line]:
                for s2 in self.linedict[line]:
                    t1 = time_between_stops(self.linedict, self.timedict, line,  s1, s2)
                    t2 = time_between_stops(self.linedict, self.timedict, line, s2, s1)
                    msg = f"line: {line}, time {t1} != {t2} for {s1} to {s2}"
                    self.assertEqual(t1,t2, msg)

    
    def test_answer_query(self):
        tramdict = {"stops": self.stopdict, "lines": self.linedict, "times": self.timedict}
        # An example of a hardcoded test for the query function. 
        # I would maybe check some strings that should give a failure too
        # Note that the parser is somewhat helpful when it parses the input

        self.assertEqual(answer_query(tramdict, "via Brunnsparken"), "1, 2, 3, 4, 5, 6, 7, 9, 10, 11")
        self.assertEqual(answer_query(tramdict, "Brunnsparken"), "Sorry, try again.")





if __name__ == '__main__':
    unittest.main()

