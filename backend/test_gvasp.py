from gvasp.common.file import OUTCAR

outcar = OUTCAR(name="OUTCAR_opt")
energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
pass
