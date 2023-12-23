from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64
from pyquery import PyQuery as pq

app = Flask(__name__)

@app.route('/')
def home():
    # 生成绘制图表所需要的数据
    x = [1, 2, 3, 4]
    y = [3, 5, 2, 6]

    # 使用Matplotlib绘制数据图表
    plt.plot(x, y)

    # 将绘制结果保存到内存中
    # img = BytesIO()
    # img = StringIO()
    plt.savefig("static/image.svg")
    # svg = pq(img.getvalue().encode("utf-8"))
    # img.seek(0)

    # 将绘制结果转成base64编码
    # plot_url = base64.b64encode(img.getvalue()).decode()

    # 渲染HTML模板并返回
    return render_template('plot.html', svg_name="static/image.svg")

if __name__ == '__main__':
    app.run()
    # home()