import requests, json
r = requests.get("https://jsonplaceholder.typicode.com/comments")

n = []

for comments in r.json():
    n.append({'id':comments['id'], 'name':comments['name']})

with open('data.json', 'w') as f:
    json.dump(n, f, indent=1)