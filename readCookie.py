import json
import os


file = open(os.path.abspath('cookies.txt'))
print(json.load(file))