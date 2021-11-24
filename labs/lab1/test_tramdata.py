import unittest
# from tramdata import *
import json
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
            self.assertIn(stop, self.stopdict, msg= stop + ' not in stopdict')

    # add your own tests here

    """ Tests that all distances are reasonable, i.e. < 20 km. """
    def test_dist_calc(self, max_dist=20):
        print("")
        dist_list = []
        for A in self.stopdict.keys():
            for B in self.stopdict.keys():
                d = distance_between_stops(self.stopdict, A, B)  # do we need to verify this function? 
                if d > max_dist:
                    print(f"FAILED with dist {d} > {max_dist} between stops {A, B}", end = "\n\n")
                    return 
        print(f"OK: distances are smaller than {max_dist}")
        print("")
    
    """ Test that all lines in text file are in db. """
    def test_lines_exist(self):
        print("")
        with open("../")










if __name__ == '__main__':
    unittest.main()

