import json
f = open('cursoFinal.json','r')
data = f.read()
f.close()
data = json.dumps(json.loads(data), ensure_ascii=False, indent=2)
f = open('cursoFinal.json','w')
f.write(data)
f.close()