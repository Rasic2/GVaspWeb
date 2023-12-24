import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def plot():
    x = [1, 2, 3, 4]
    y = [3, 5, 2, 6]

    line_width = 1
    if request.method == "POST":
        line_width = request.form['lineWidth']

    plt.plot(x, y, color="r", linewidth=line_width)
    plt.savefig("static/image.svg")
    plt.close()

    return render_template('plot.html', svg_name="static/image.svg")


if __name__ == '__main__':
    app.run(debug=True)
