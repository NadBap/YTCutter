import json
with open("Util/user-interface.json", 'r') as file:
    hello = json.load(file)

print(hello["Loading Bar"]["Font-color"])