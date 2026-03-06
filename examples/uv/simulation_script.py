# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "stdpopsim",
# ]
# ///

import stdpopsim

species = stdpopsim.get_species("HomSap")
model = species.get_demographic_model("PapuansOutOfAfrica_10J19")
contig = species.get_contig("chr22")
engine = stdpopsim.get_engine("msprime")

samples = {
    "YRI": 30,
    "NeaA": 30,
    "DenA": 30,
}

ts = engine.simulate(model, contig, samples)

print(f"Num trees: {ts.num_trees:,}")
print(f"Num samples: {ts.num_samples}")
print(f"Sequence length: {ts.sequence_length:,.0f} bp")
print(f"Num mutations: {ts.num_mutations:,}")

ts.dump("archaic_simulation.trees")
print("Saved to archaic_simulation.trees")
