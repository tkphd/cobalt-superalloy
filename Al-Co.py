# -*- coding: utf-8 -*-

from pycalphad import ConditionError, Database, Model, calculate, equilibrium
from pycalphad.plot.utils import phase_legend
from pycalphad.core.utils import filter_phases, unpack_components
import pycalphad.variables as v
import matplotlib.pyplot as plt
import numpy as np

tdb = Database("Wang_AlCoW.tdb")
elems = ["AL", "CO", "VA"]
temp = 1200

"""
# Possible phases with ["AL", "CO", "W", "VA"]:
# >>> ["AL12W", "AL2W", "AL3CO", "AL4W", "AL5CO2", "AL5W", "AL77W23", "AL9CO2", "BCC_B2", "CHI", "HCP_A3", "L12_FCC", "LIQUID", "MAL13CO4", "MU", "OAL13CO4", "YAL13CO4"]
# Possible phases with ["AL", "CO", "W", "VA"]:
# >>> ["AL3CO", "AL5CO2", "AL9CO2", "BCC_B2", "CHI", "HCP_A3", "L12_FCC", "LIQUID", "MAL13CO4", "MU", "OAL13CO4", "YAL13CO4"]

elems = sorted(unpack_components(tdb, elems))
phases = filter_phases(tdb, elems) # ["AL12W"]
if len(phases) == 0:
    raise ConditionError("There are no phases in the Database that can be active with components {0}".format(elems))
else:
    print("Possible phases:", phases)
"""

# phases = ["FCC_A1", "L12_FCC", "LIQUID"]
phases = ["FCC_A1", "L12_FCC", "LIQUID"]
legend_handles, colorlist = phase_legend(phases)

fig = plt.figure(figsize=(9, 6))
ax = fig.gca()
ax.set_xlabel("$x_{\\mathrm{Al}}$")
ax.set_ylabel("$\\mathcal{G}$", rotation=0)

for name in phases:
    result = calculate(tdb, elems, name, P=101325, T=temp, output="GM")
    ax.scatter(result.X.sel(component="AL"), result.GM, marker=".", s=5, color=colorlist[name.upper()])
    ax.set_xlim((0.4, 0.6))
    ax.set_ylim((-90100, -89000))
    ax.legend(handles=legend_handles, loc="center left", bbox_to_anchor=(1, 0.6))

plt.savefig("diagram.png", dpi=400, bbox_inches="tight")
plt.close()

eqm = equilibrium(tdb, elems, "L12_FCC", {v.X("AL"): (8e-13,1.2e-12,1e-15), v.T: temp, v.P: 101325},
                                    output="degree_of_ordering")

print(eqm)

plt.title("Al-Co: Degree of FCC ordering [T={0} K]".format(temp))
plt.xlabel("$x_{\\mathrm{Al}}$")
plt.ylabel("Degree of ordering")
# Generate a list of all indices where B2 is stable
phase_indices = np.nonzero(eqm.Phase.values == "L12_FCC")
# phase_indices[2] refers to all composition indices
# We know this because pycalphad always returns indices in order like P, T, X
plt.semilogx(np.take(eqm["X_AL"].values, phase_indices[2]), eqm["degree_of_ordering"].values[phase_indices])
plt.savefig("disorder.png", dpi=400, bbox_inches="tight")
plt.close()
