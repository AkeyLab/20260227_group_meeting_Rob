# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "msprime",
#     "demes",
# ]
# ///
"""Simulate chromosome 22 under the PapuansOutOfAfrica_10J19 demographic model."""

import demes
import msprime

# Load demography
graph = demes.load("demography.yaml")
demography = msprime.Demography.from_demes(graph)

# Determine archaic sampling times from the demes graph
deme_map = {d.name: d for d in graph.demes}
nea_time = deme_map["NeaA"].end_time
den_time = deme_map["DenA"].end_time

print(f"Sampling NeaA at time {nea_time}")
print(f"Sampling DenA at time {den_time}")

# Sample 30 diploid individuals from each of 3 populations
samples = [
    msprime.SampleSet(30, population="YRI", time=0),
    msprime.SampleSet(30, population="NeaA", time=nea_time),
    msprime.SampleSet(30, population="DenA", time=den_time),
]

# Chromosome 22 parameters
seq_length = 50_818_468  # bp (GRCh38)
recomb_rate = 1.4e-8     # per bp per generation

ts = msprime.sim_ancestry(
    samples=samples,
    demography=demography,
    sequence_length=seq_length,
    recombination_rate=recomb_rate,
    random_seed=42,
)

ts.dump("chr22.trees")
print(f"Wrote chr22.trees ({ts.num_trees} trees, {ts.num_samples} samples)")
