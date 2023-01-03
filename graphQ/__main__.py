import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="filepath of introspection")
args = ap.parse_args()

print(args)
