# -*- coding: utf-8 -*-

from pycalphad import ConditionError, Database, Model, calculate, equilibrium
from pycalphad.plot.utils import phase_legend
from pycalphad.core.utils import filter_phases, unpack_components
import pycalphad.variables as v
import matplotlib.pyplot as plt
import numpy as np

tdb = Database("Wang_AlCoW.tdb")
elems = ["AL", "CO", "VA"]
temp = 300
atm = 101325

phases = ["LIQUID", "L12_FCC", "FCC_A1"]
legend_handles, colorlist = phase_legend(phases)

fig = plt.figure(figsize=(9, 6))
ax = fig.gca()
ax.set_xlabel("$x_{\\mathrm{Al}}$")
ax.set_ylabel("$\\mathcal{G}$", rotation=0)

for name in phases:
    result = calculate(tdb, elems, name, P=atm, T=temp, output="GM")
    ax.scatter(result.X.sel(component="AL"), result.GM, marker=".", s=5, color=colorlist[name.upper()])
    ax.set_xlim((0, 1))
    #ax.set_ylim((-90100, -89000))
    ax.legend(handles=legend_handles, loc="center left", bbox_to_anchor=(1, 0.6))

plt.savefig("diagram.png", dpi=400, bbox_inches="tight")
plt.close()

eqm = equilibrium(tdb, elems, "L12_FCC", {v.X("AL"): (0, 1, 0.01), v.T: temp, v.P: atm},
                                    output="degree_of_ordering")

plt.title("Al-Co: Degree of FCC ordering [T={0} K]".format(temp))
plt.xlabel("$x_{\\mathrm{Al}}$")
plt.ylabel("Degree of ordering")

# Generate a list of all indices where L12 is stable
phase_indices = np.nonzero(eqm.Phase.values == "L12_FCC")
# phase_indices[2] refers to all composition indices
# We know this because pycalphad always returns indices in order like P, T, X
plt.plot(np.take(eqm["X_AL"].values, phase_indices[2]), eqm["degree_of_ordering"].values[phase_indices])
plt.xlim([0,1])
plt.savefig("disorder.png", dpi=400, bbox_inches="tight")
plt.close()
