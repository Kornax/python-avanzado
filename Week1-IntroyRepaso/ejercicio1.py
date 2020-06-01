# Escribir una función que reciba un nombre de usuario y
# un password e imprima en pantalla la cantidad de
# productos que tiene asociados el usuario y los nombres de
# ese productos. En una primera instancia el pass puede
# ser texto plano, luego se debe mandar la clave
# encriptada y dentro del programa desencriptar.

#Librerias
import requests
import json

#Encriptado
from cryptography.fernet import Fernet
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)

#Tomo usuario y password que vienen en la función (si es necesario, desencriptar pass).
user = input("Ingrese Usuario:")
pwd = input("Ingrese Password:")

#Desencriptado de password
pwd = (cipher_suite.decrypt(pwd.encode("utf-8"))).decode("utf-8 ")


#Armo url para hacer post a login.vera ...

url_token = "https://login.vera.com.uy/oidc/accessToken"
url_products = "https://api.antel.com.uy/users/" + user + "/products"

params = { 
    "username": user,
    "password": pwd,
    "grant_type":"password",
    "client_id":"urn:antel:mdm:system:pi"
}

r = requests.post(url_token, params=params)

# Cargo el resultado en un Json, me quedo con el valor access_token

if r.status_code == 200: 
    data = json.loads(r.text)
    token = data['access_token']
else:
    print("Result:",r.status_code)
    exit()

print("Token:", token)

# Armo header para mandar en el request a la API de usuarios, incluyendo el token obtenido en el paso anterior:

header_auth={"Authorization": "Bearer " + token}
r = requests.get(url_products, verify=False, headers=header_auth)

# Cargo el resultado en un Json que luego vuelco a una variable de Py

if r.status_code == 200: 
    data = json.loads(r.text)
    products = data['products']
else:
    print("Result:",r.status_code)
    exit()

# Usando esa variable, itero en la lista de products (lista de diccionarios) 
# y para cada elemento de la lista accedo a la clave productSpecLabel, 
# que es donde está el nombre del producto.
print("Usuario: ", user)

print("Cantidad de Productos: ", len(products) )

for p in products:
    print(products["productSpecLabel"])