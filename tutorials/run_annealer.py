import add_path

from Benchmarking.Algorithms.Annealer import Annealer
from Benchmarking.DataStructures.Configuration import getConfiguration

evolution_steps = 200


def run_annealer(benchmark: str, compression_type: str, evolution_steps: int, multi_change: bool = False):
    conf = getConfiguration(compression_type=compression_type,
                            compression_types=[compression_type])
    a = Annealer(configuration=conf, benchmark=benchmark,
                 multi_change=multi_change)
    a.evolve(steps=evolution_steps)


# LHCb
run_annealer("lhcb", "lz4", evolution_steps, multi_change=False)
run_annealer("lhcb", "zstd", evolution_steps, multi_change=False)

# Atlas
run_annealer("atlas", "lz4", evolution_steps, multi_change=False)
run_annealer("atlas", "zstd", evolution_steps, multi_change=False)

# CMS
run_annealer("cms", "lz4", evolution_steps, multi_change=False)
run_annealer("cms", "zstd", evolution_steps, multi_change=False)

# H1
run_annealer("h1", "lz4", evolution_steps, multi_change=False)
run_annealer("h1", "zstd", evolution_steps, multi_change=False)
