import os
import shutil
import time
from hashlib import md5
from pathlib import Path

from flask import Flask, request, send_from_directory
from flask_cors import cross_origin, CORS
from gvasp.common.file import OUTCAR, LOCPOT, CONTCAR
from gvasp.common.plot import DOSData, PESData

app = Flask(__name__, static_folder="static")
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

colors = ['#01545a', '#ed0345', '#ef6932', '#710162', '#017351', '#03c383', '#aad962', '#fbbf45',
          '#a12a5e', '#047df6', '#FFFF33', 'FF2CF2', '#F1D1E1', '#E6FFE7']

# 创建保存文件的目录
UploadPath = Path(UPLOAD_FOLDER)
UploadPath.mkdir(exist_ok=True)

# 获取当前时间
now = time.time()

# 遍历uploads目录下的文件和子目录
for file_path in UploadPath.iterdir():
    # 检查文件的最后修改时间
    file_mtime = file_path.stat().st_mtime

    # 如果文件超过一天（24小时没有修改），则删除
    if now - file_mtime > 24 * 60 * 60:
        if file_path.is_file():
            file_path.unlink()
            print(f"Deleted file {file_path}")
        elif file_path.is_dir():
            shutil.rmtree(file_path)
            print(f"Deleted directory {file_path}")


# @app.route("/")
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')
#
#
# @app.route("/<path:path>")
# def serve_static(path):
#     return send_from_directory(app.static_folder, path)


@app.route('/api/upload', methods=['POST'])
@cross_origin(origins="*")
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        chunk_index = request.form['chunkIndex']
        total_chunks = request.form['totalChunks']

        if request.form['filename'] == '':
            return '没有选择文件'
        try:
            original_filename = request.form['filename']
            md5_object = md5()
            md5_object.update(original_filename.encode('utf-8'))
            new_filename = md5_object.hexdigest() + os.path.splitext(original_filename)[1]
            file_path = UploadPath / new_filename
            file_part_path = str(file_path) + f".{chunk_index}"
            file.save(file_part_path)

            with open(file_part_path, "r") as f:
                file_line_count = len(f.readlines())
            file_content = None

            if int(chunk_index) == int(total_chunks) - 1:
                with open(file_path, 'wb') as output_file:
                    for i in range(int(total_chunks)):
                        with open(UploadPath / f"{new_filename}.{i}", 'rb') as part_file:
                            output_file.write(part_file.read())
                        os.remove(UploadPath / f"{new_filename}.{i}")

                try:
                    contcar = CONTCAR(file_path)
                    _ = contcar.structure
                    file_content = ''.join(contcar.strings)
                except Exception:
                    file_content = None
            return {"filePath": str(file_path.relative_to("./")), "fileContent": file_content,
                    "fileLineCount": file_line_count}
        except Exception as e:
            return '文件上载过程中出错: {}'.format(str(e))
    else:
        return '请求方法不允许'


@app.route('/api/get_opt_data', methods=['POST'])
@cross_origin(origins="*")
def plot_opt():
    params = request.get_json()
    outcar = OUTCAR(name=params['outcarPath'])
    energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
    force = [[step + 1, f] for step, f in enumerate(outcar.force)]
    data = {
        "energy": energy,
        "force": force
    }

    return data


@app.route('/api/get_ep_data', methods=['POST'])
@cross_origin(origins="*")
def plot_ep():
    params = request.get_json()
    locpot = [[x, l] for x, l in zip(*LOCPOT(name=params['locpotPath']).line_potential(direction='z'))]
    data = {
        "locpot": locpot
    }

    return data


@app.route('/api/get_dos_data', methods=['POST'])
@cross_origin(origins="*")
def plot_dos():
    params = request.get_json()
    multi_atoms = [list(map(lambda x: int(x), atom['input'].split(','), )) for atom in params['atoms']]
    orbitals = [atom['orbitals'] for atom in params['atoms']]
    multi_orbitals = list(map(lambda x: None if not len(x) else x, orbitals))
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


@app.route('/api/get_pes_data', methods=['POST'])
@cross_origin(origins="*")
def plot_pes():
    defaultDict = {'type': 'line', 'smooth': False, 'encode': {'x': 0, 'y': 1}, 'symbol': 'none'}
    params = request.get_json()
    front_data = params['data']
    server_data = []

    for index, data in enumerate(front_data):
        pes_data = PESData(data)
        parse_data = pes_data.convert_sd()
        solid_line = [[[x[0], y[0]], [x[1], y[1]]] for x, y in zip(parse_data[0], parse_data[1])]
        dashed_line = [[[x[0], y[0]], [x[1], y[1]]] for x, y in zip(parse_data[2], parse_data[3])]
        singleSolidRoute = [{**defaultDict, 'name': f'L{index}', 'data': data, 'lineStyle': {'type': 'solid'}, } for
                            data in solid_line]
        singleDashedRoute = [{**defaultDict, 'name': f'L{index}', 'data': data, 'lineStyle': {'type': 'dashed'}, } for
                             data in dashed_line]
        singleRoute = singleDashedRoute + singleSolidRoute
        server_data += singleRoute
    return server_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
