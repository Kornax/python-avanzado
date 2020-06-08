from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

WORKER = {
    "1": {
        "first_name": "Gustavo",
        "last_name": "Signorele",
        "timestamp": get_timestamp()
    },
    "2": {
        "first_name": "Rodrigo",
        "last_name": "Pérez",
        "timestamp": get_timestamp()
    }
}

def read():
    # Funcion que al request /api/worker con el listado de funcionarios
    return [WORKER[key] for key in sorted (WORKER.keys())]


def read_by_id(id):
    if id not in WORKER.keys():
        return "No se encuentra el funcionario con el id {id_worker} especificado".format(id_worker=id)
    return WORKER[id]