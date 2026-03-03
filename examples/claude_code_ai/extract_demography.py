# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "stdpopsim",
#     "demes",
# ]
# ///
"""Extract the PapuansOutOfAfrica_10J19 demography to a demes YAML file."""

import demes
import stdpopsim

species = stdpopsim.get_species("HomSap")
model = species.get_demographic_model("PapuansOutOfAfrica_10J19")

graph = model.model.to_demes()
demes.dump(graph, "demography.yaml")

print("Wrote demography.yaml")
print()
print(f"{'Population':<15} {'Start Time':>12} {'End Time':>12}")
print("-" * 41)
for deme in graph.demes:
    print(f"{deme.name:<15} {deme.start_time:>12.1f} {deme.end_time:>12.1f}")
