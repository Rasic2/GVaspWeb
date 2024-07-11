import os

from gvasp.common.file import OUTCAR, LOCPOT, XDATCAR
from gvasp.common.plot import DOSData, PESData


def get_opt_data():
    outcar = OUTCAR(name="OUTCAR")
    energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]


def get_ep_data():
    locpot = [[x, l] for x, l in zip(*LOCPOT(name="LOCPOT").line_potential(direction='z'))]


def get_dos_data():
    dosdata = DOSData(dos_file="/Users/hui_zhou/Project/flask-js/backend/uploads/f147e2d6-c1b4-424f-8f74-ccb47cb43295",
                      pos_file="/Users/hui_zhou/Project/flask-js/backend/uploads/41cbc9aa-f946-40b9-8c79-764aca89b67b")
    real_data = dosdata.get_data(atoms=[1, 2], orbitals=None)
    x_data = dosdata.total_dos.index.values
    y_up_data = dosdata.total_dos['tot_up'].values
    y_down_data = dosdata.total_dos['tot_down'].values
    total_dos = [[[x, y] for x, y in zip(x_data, y_up_data)], [[x, y] for x, y in zip(x_data, y_down_data)]]


def get_pes_data():
    data = [10, 20, 15, 25, 20]
    pes_data = PESData(data)
    parse_data = pes_data.convert_sd()
    solid_line = [[[x[0], y[0]], [x[1], y[1]]] for x, y in zip(parse_data[0], parse_data[1])]
    dashed_line = [[[x[0], y[0]], [x[1], y[1]]] for x, y in zip(parse_data[2], parse_data[3])]
    pass


def get_structures():
    xdatcar = XDATCAR("XDATCAR")
    structures = xdatcar.structure
    contents = []
    for structure in structures:
        structure.write_POSCAR(name="temp")
        with open("temp", "r") as f:
            contents.append(f.read())
        os.system("rm -rf temp")
    pass


if __name__ == '__main__':
    # get_pes_data()
    # get_opt_data()
    get_structures()
