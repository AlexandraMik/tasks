import requests, re, json
r = requests.get("https://habr.com/ru/all/")

t = r.text
prog = re.compile(r'\/ru\/[a-zA-z,\/,0-9]*')
m = prog.findall(t)
m = ["https://habr.com" + i for i in m]
y = sorted(set(m), key=lambda d:  m.index(d))
with open('datahabr.json', 'w') as f:
    json.dump(y, f, indent=0)