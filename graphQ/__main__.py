import argparse
import json
from graphQ import Graph

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="filepath of introspection")
ap.add_argument("-u", "--url", help="url of introspection")
args = ap.parse_args()

if args.file:
    with open(args.file) as f:
        data = json.load(f)
        breakpoint()
if args.url:
    g = Graph(url=args.url)
    cycles = g.detect_cycles(top_only=False)
    breakpoint()