import os
import sqlite3
import uuid

from flask import Flask, request
from flask_cors import cross_origin, CORS
from gvasp.common.file import OUTCAR, LOCPOT, CONTCAR
from gvasp.common.plot import DOSData

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 设置最大文件上传大小为 100MB

# 创建保存文件的目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 初始化数据库
conn = sqlite3.connect('file_mapping.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS files
             (id INTEGER PRIMARY KEY, original_filename TEXT, new_filename TEXT)''')
conn.commit()
conn.close()


@app.route('/api/upload', methods=['POST'])
@cross_origin(origins="*")
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        files = request.files.getlist('file')
        conn = sqlite3.connect('file_mapping.db')
        c = conn.cursor()
        file = files[0]

        if file.filename == '':
            return '没有选择文件'
        try:
            original_filename = file.filename
            # 查询数据库，检查文件名是否已经存在
            c.execute("SELECT * FROM files WHERE original_filename=?", (original_filename,))
            existing_file = c.fetchone()
            if existing_file:
                new_filename = existing_file[2]
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            else:
                # 生成唯一的文件名
                new_filename = str(uuid.uuid4()) + os.path.splitext(original_filename)[1]
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(file_path)
                # 存储原始文件名和新文件名的关联关系到数据库
                c.execute("INSERT INTO files (original_filename, new_filename) VALUES (?, ?)",
                          (original_filename, new_filename))
            conn.commit()
            try:
                contcar = CONTCAR(file_path)
                _ = contcar.structure
                file_content = ''.join(contcar.strings)
            except Exception:
                file_content = None
            return {"filePath": file_path, "fileContent": file_content}
        except Exception as e:
            return '文件上载过程中出错: {}'.format(str(e))
        finally:
            conn.close()
    else:
        return '请求方法不允许'


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


@app.route('/api/get_dos_data', methods=['POST'])
@cross_origin(origins="*")
def plot_dos():
    params = request.get_json()
    dos_data = DOSData(dos_file=params['doscarPath'], pos_file=params['contcarPath'])
    x_data = dos_data.total_dos.index.values
    y_up_data = dos_data.total_dos['tot_up'].values
    y_down_data = dos_data.total_dos['tot_down'].values
    total_dos = [[[x, y] for x, y in zip(x_data, y_up_data)], [[x, y] for x, y in zip(x_data, y_down_data)]]
    data = {
        "total_dos": total_dos
    }

    return data


if __name__ == '__main__':
    app.run(debug=True)
