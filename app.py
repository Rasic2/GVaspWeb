import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # 生成绘制图表所需要的数据
    x = [1, 2, 3, 4]
    y = [3, 5, 2, 6]

    # 使用Matplotlib绘制数据图表
    plt.plot(x, y)

    plt.savefig("static/image.svg")

    return render_template('plot.html', svg_name="static/image.svg")


if __name__ == '__main__':
    app.run()
