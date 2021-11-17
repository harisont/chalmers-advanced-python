import json
import csv
import re


def build_tram_stops(PATH = '../data/tramstops.json'):
    try:
        with open(PATH) as f:
            raw_data = json.load(f)
            locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}
        print(locs)
    except FileNotFoundError:
        print(f"Data base file not found on relative path: {PATH}")
    # locs = {k: {'lat': v["position"][0], 'long': v["position"][1]} for (k, v) in raw_data.items()}


def build_tram_lines(PATH = '../data/tramlines.txt'):
    lines = {}
    try:
        with open(PATH, encoding='utf8') as f:
            raw_data = []

            # I don't know how to split it!!!!!

            for line in f:
                raw_data.append(line.split("  ")[0])
            lines_dict = {}
        print(raw_data)
    except FileNotFoundError:
        print(f"Data base file not found on relative path: {PATH}")


if __name__ == "__main__":
    build_tram_stops()
    build_tram_lines()
