from gvasp.common.file import OUTCAR, LOCPOT

outcar = OUTCAR(name="OUTCAR_opt")
energy = [[step + 1, e] for step, e in enumerate(outcar.energy)]
locpot = [[x, l] for x, l in zip(*LOCPOT(name="LOCPOT").line_potential(direction='z'))]
pass
