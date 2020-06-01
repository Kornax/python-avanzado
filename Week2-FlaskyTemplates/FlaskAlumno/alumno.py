from flask import Flask,request,jsonify,Response
import json

app = Flask(__name__)

dbPath = "database.txt"

def writeAlumnos(data):
    db = readAlumnos()
    try:
        with open(dbPath,'a') as f:
            for d in data:
                #l = [l for l in db if l["id"] == d["id"]]
                if d["id"] and d["nombre"] and d["estado"]: 
                        f.write(json.dumps(d))
                else:
                    return 500
            return 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def readAlumnos():
    data = []
    try:
        with open(dbPath,"r") as f:
            lines = f.readlines()
            for d in lines:
                data.append(json.loads(d))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return data


@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    if request.method == 'GET':
        #Obtener todos los alumnos. Debe aceptar también: GET /alumnos?estado=[aprobado|reprobado|pendiente]
        estado = request.args.get('estado')
        data = readAlumnos()
        result = []
        for d in data:
            if d["estado"] == estado:
                result.append(d)    
        if result:
            r = jsonify(result)
            return r, 200
        else: 
            return "" , 204
    elif request.method == 'POST':
        # Dar de alta un alumno (o varios). Los datos deben enviarse vía Json son, al menos:
        # nombre, ci, estado. Los datos pueden guardarse en BD o bien, en un archivo
        data = request.json
        return writeAlumnos(data)

@app.route('/alumnos/<id>', methods=['GET', 'PUT', 'DELETE'])
def alumnosId(id):
    if request.method == 'GET':
        #Obtener el alumno identificado con el id especificado (puede ser la CI)
        data = readAlumnos()
        for d in data:
            if d["id"] == id:
                result = d
        r = jsonify(result)
        r.status_code = 200
        return r
    elif request.method == 'PUT':
        #Dar de alta un alumno (o varios). Los datos deben enviarse vía Json son, 
        # al menos, nombre, ci, estado. Los datos pueden guardarse en BD o bien, en un archivo.
        r = jsonify({"put":'success'})
        return r
    elif request.method == 'DELETE':
        # Borrar el alumnos el id especificado
        r = jsonify({"delete":'success'})
        return r