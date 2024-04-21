from flask import Flask
from flask_cors import cross_origin
from gvasp.common.file import OUTCAR, LOCPOT

app = Flask(__name__)


@app.route('/api/getdata', methods=['GET'])
@cross_origin(origins="*")
def plot_opt():
    outcar = OUTCAR(name="OUTCAR")
    energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
    force = [[step + 1, f] for step, f in enumerate(outcar.force)]
    data = {
        "energy": energy,
        "force": force
    }

    return data


@app.route('/api/get_ep_data', methods=['GET'])
@cross_origin(origins="*")
def plot_ep():
    locpot = [[x, l] for x, l in zip(*LOCPOT(name="LOCPOT").line_potential(direction='z'))]
    data = {
        "locpot": locpot
    }

    return data


if __name__ == '__main__':
    app.run(debug=True)
