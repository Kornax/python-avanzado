import requests

r = requests.get('http://www.antel.com.uy')

print(r.status_code) # 200 (OK)
print(r.text) #El HTML de la página de Antel