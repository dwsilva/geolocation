from flask import Flask, request, jsonify
from src.app.Database import Database

db = Database(user='root', password='root', host='localhost')

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'Api online!'


@app.route('/get', methods=['GET'])
def get_data():
    registros = db.select_all_devices()
    return jsonify(registros)


@app.route('/get/device/<int:id>', methods=['GET'])
def get_devide(id):
    select = db.select_id_device(id)
    if select:
        return jsonify(select)
    elif not select:
        return 'Id nof found!!'
    else:
        return select.pgerror


@app.route('/create', methods=['POST'])
def create_data():
    request_data = request.get_json()
    result = []
    for item in request_data:
        select = db.insert_db(item["id"], item["lat"], item["long"])
        if select == 1:
            result.append(item)
        else:
            return select.pgerror
    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
