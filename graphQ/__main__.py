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
    trimmed,mapping,matrix = g.to_matrix()
    matrix.SCC()
    # matrix.sub_SCC()
    cycles = matrix.sub_cycles or matrix.cycles
    if isinstance(cycles,list):
        result = []
        for cycle in cycles:
            result.append([trimmed[c] for c in cycle])
    if isinstance(cycles,dict):
        result = {}
        for cycle in cycles:
            mapped_cycle = tuple(trimmed[c] for c in cycle)
            result[mapped_cycle] = set(tuple(trimmed[c] for c in sub_cycle) for sub_cycle in cycles[cycle])
    breakpoint()