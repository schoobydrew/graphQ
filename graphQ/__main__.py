import argparse
import json
from graphQ import Graph

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="filepath of introspection")
ap.add_argument("-u", "--url", help="url of introspection")
ap.add_argument("-c", "--cycles", default=False, action="store_true", help="detect cycles")
ap.add_argument("-tc", "--top-cycles", default=False, action="store_true", help="only detect top level cycles")
ap.add_argument("-p", "--poi", default=False, action="store_true", help="find points of interest")
ap.add_argument("-pr", "--poi-regex", help="regex to find points of interest")
args = ap.parse_args()

g = None
if args.file:
    with open(args.file) as f:
        data = json.load(f)
if args.url:
    g = Graph(url=args.url)
if not g:
    print("FILE or URL must be set, graph schema not loaded")
    exit(0)
if args.cycles:
    cycles = g.detect_cycles(top_only=args.top_cycles)
    print(cycles)
if args.poi:
    poi = g.get_sensitive(pattern=args.poi_regex)
    print(poi)