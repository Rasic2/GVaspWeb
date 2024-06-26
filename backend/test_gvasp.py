from gvasp.common.file import OUTCAR, LOCPOT
from gvasp.common.plot import DOSData

outcar = OUTCAR(name="OUTCAR")
energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
locpot = [[x, l] for x, l in zip(*LOCPOT(name="LOCPOT").line_potential(direction='z'))]
dosdata = DOSData(dos_file="/Users/hui_zhou/Project/flask-js/backend/uploads/f147e2d6-c1b4-424f-8f74-ccb47cb43295",
                  pos_file="/Users/hui_zhou/Project/flask-js/backend/uploads/41cbc9aa-f946-40b9-8c79-764aca89b67b")
x_data = dosdata.total_dos.index.values
y_up_data = dosdata.total_dos['tot_up'].values
y_down_data = dosdata.total_dos['tot_down'].values
total_dos = [[[x,y] for x,y in zip(x_data,y_up_data)],[[x,y] for x,y in zip(x_data,y_down_data)]]
pass
