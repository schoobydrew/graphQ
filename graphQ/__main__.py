import argparse
import json
import yaml
from graphQ import Graph

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="filepath of introspection")
ap.add_argument("-u", "--url", help="url of introspection")
ap.add_argument(
    "-c", "--cycles", default=False, action="store_true", help="detect cycles"
)
ap.add_argument(
    "-tc",
    "--top-cycles",
    default=False,
    action="store_true",
    help="only detect top level cycles",
)
ap.add_argument(
    "-p", "--poi", default=False, action="store_true", help="find points of interest"
)
ap.add_argument("-pr", "--poi-regex", help="regex to find points of interest")
ap.add_argument("-s", "--save", help="filepath to write introspection")
ap.add_argument("-H", "--headers", action="append", default=[])
args = ap.parse_args()

g = None
if args.file:
    g = Graph(file_path=args.file)
if args.url:
    g = Graph(url=args.url, additional_headers=yaml.safe_load("\n".join(args.headers)))
if not g:
    print("FILE or URL must be set, graph schema not loaded")
    exit(0)
if args.save:
    with open(args.save, "w") as f:
        json.dump(g.introspection_data, f)
if args.cycles:
    cycles = g.detect_cycles(top_only=args.top_cycles)
    print(f"Found {len(cycles)} composite cycles")
    for idx, cycle in enumerate(cycles):
        print(idx)
        print(cycle)
        if not args.top_cycles:
            sub_cycles = cycles[cycle]
            print(f"Found {len(sub_cycles)} sub cycles")
            for sidx, sub_cycle in enumerate(sub_cycles):
                print(f"{idx}-{sidx}")
                print(sub_cycle)

if args.poi:
    poi = g.get_sensitive(pattern=args.poi_regex)
    print("Interesting Functions Names")
    for root, funcs in poi["Interesting Functions Names"].items():
        for func in funcs:
            print(f"\t{root} - {func}")
    print("Interesting Field Names")
    for node, fields in poi["Interesting Field Names"].items():
        for field in fields:
            print(f"\t{node} - {field}")
    print("Interesting Node Names")
    for node in poi["Interesting Node Names"]:
        print(f"\t{node}")
