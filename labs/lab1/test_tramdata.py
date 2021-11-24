import unittest
from tramdata import *
from math import acos, cos, sin, radians
TRAM_FILE = './tramnetwork.json'


def distance(lat1, lon1, lat2, lon2):
    theta = lon1 - lon2
    dist = acos(sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(theta)))
    return dist * 111.9


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg= stop + ' not in stopdict')

    # add your own tests here
    def test_stops_range(self, max_dist):
        dist_list = []
        for A in self.stopdict:
            for B in self.stopdict:
                dist_list.append(distance(A[lat], A[lon], B[lat], B[lon]) < max_dist)
        if max(dist_list) < max_dist:
            print(f"test ok: distances are smaller than {max_dist}")
        else:
            print(f"test failed: distances are larger than {max_dist}")





if __name__ == '__main__':
    unittest.main()

