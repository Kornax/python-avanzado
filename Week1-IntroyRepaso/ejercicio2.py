
import requests
import json

url = "http://www.montevideo.gub.uy/ubicacionesRest/calles/"

street = input("Ingresar calle: ")

params = {
    "nombre": street,
}

headers = {
    'User-Agent': 'Mozilla/5.0',
}

r = requests.get(url, params = params, headers= headers)

if r.status_code == 200:
    data = json.loads(r.text)
else: 
    print("Resultado: ", r.status_code)
    exit()

for s in data:
    print(s["nombre"])