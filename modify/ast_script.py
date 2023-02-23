import ast
from pprint import pprint

r = open('to_parse.py', 'r')
t = ast.parse(r.read())
pprint(ast.dump(t, indent=4))
