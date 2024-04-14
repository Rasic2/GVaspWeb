from flask import Flask
from flask_cors import cross_origin
from gvasp.common.file import OUTCAR

app = Flask(__name__)


@app.route('/api/getdata', methods=['GET'])
@cross_origin(origins="*")
def plot():
    outcar = OUTCAR(name="OUTCAR_opt")
    energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
    data = {
        "data": energy
    }

    return data


if __name__ == '__main__':
    app.run(debug=True)
