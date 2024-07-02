import os
import sqlite3
import uuid

from flask import Flask, request, send_from_directory
from flask_cors import cross_origin, CORS
from gvasp.common.file import OUTCAR, LOCPOT, CONTCAR
from gvasp.common.plot import DOSData

app = Flask(__name__, static_folder="static")
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


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


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
    colors = ['#01545a', '#ed0345', '#ef6932', '#710162', '#017351', '#03c383', '#aad962', '#fbbf45',
              '#a12a5e', '#047df6', '#FFFF33', 'FF2CF2', '#F1D1E1', '#E6FFE7']
    params = request.get_json()
    multi_atoms = [list(map(lambda x: int(x), atom['input'].split(','), )) for atom in params['atoms']]
    orbitals = [atom['orbitals'] for atom in params['atoms']]
    multi_orbitals = [None for item in orbitals if not len(item)]
    dos_data = DOSData(dos_file=params['doscarPath'], pos_file=params['contcarPath'], magnification=1)

    default_style = {'type': 'line',
                     'label': {'show': False}}
    data = []
    for index, (atoms, orbitals, color) in enumerate(zip(multi_atoms, multi_orbitals, colors)):
        inner_data = dos_data.get_data(atoms=atoms, orbitals=orbitals)
        color_dict = {'lineStyle': {'color': color},
                      'itemStyle': {'color': color}}
        up_dict = {'name': f'L{index + 1}_up', 'data': [[x, y] for x, y in zip(inner_data.energy, inner_data.up)]}
        down_dict = {'name': f'L{index + 1}_down', 'data': [[x, y] for x, y in zip(inner_data.energy, inner_data.down)]}
        data.append({**default_style, **up_dict, **color_dict})
        data.append({**default_style, **down_dict, **color_dict})

    if params['checkedTDOS']:
        color_dict = {'lineStyle': {'color': '#000000'},
                      'itemStyle': {'color': '#000000'}}
        x_data = dos_data.total_dos.index.values
        y_up_data = dos_data.total_dos['tot_up'].values
        y_down_data = dos_data.total_dos['tot_down'].values
        total_dos = [[[x, y] for x, y in zip(x_data, y_up_data)], [[x, y] for x, y in zip(x_data, y_down_data)]]
        tup_dict = {'name': 'TDOS_up', 'data': total_dos[0]}
        tdown_dict = {'name': 'TDOS_down', 'data': total_dos[1]}
        data.append({**default_style, **tup_dict, **color_dict})
        data.append({**default_style, **tdown_dict, **color_dict})

    return {"series": data}


if __name__ == '__main__':
    app.run(debug=True)
