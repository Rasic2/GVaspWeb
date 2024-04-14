from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/api/getdata', methods=['GET'])
@cross_origin(origins="*")
def plot():
    data = {
        "data": [
            [20, 120],
            [50, 200],
            [40, 50]
        ]
    }

    return data


if __name__ == '__main__':
    app.run(debug=True)
