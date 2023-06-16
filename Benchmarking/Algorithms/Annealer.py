# %%

# root [12] auto ntuple = ROOT::Experimental::RNTupleReader::Open("DecayTree" , "generated/B2HHH~none.ntuple")
# root [13] ntuple->PrintInfo(ROOT::Experimental::ENTupleInfo::kStorageDetails)

from dataclasses import dataclass
from datetime import datetime
import numpy as np
from random import random

from Benchmarking.DataStructures.Configuration import Configuration
from Benchmarking.benchmark_utils import get_size_decrease, get_throughput_increase, get_memory_usage_decrease, get_performance

from Benchmarking.Algorithms.Walker import Walker

# %%


@dataclass
class Annealer(Walker):
    # Annealer parameters
    temperature_const: float = 2.5
    iteration: int = 0

    def get_class_name(self) -> str:
        return "Annealer"

    def get_temperature(self, iteration: int) -> float:
        """ Get temperature based on the current iteration

        Args:
            iteration (int)

        Returns:
            float
        """
        return self.temperature_const / np.log(iteration + 2)

    def get_probability(self, iteration: int, c: float) -> float:
        """ Get the probability of accepting a change based on 
        the current iteration and the difference in performance

        Args:
            iteration (int)
            c (float): The difference between the performance of 
                       the new and old configuration

        Returns:
            float
        """
        return np.exp(c / self.get_temperature(iteration))

    def is_accepted(self, performance: float, iteration: int) -> bool:
        # Determine if new configuration will be accepted
        c = performance - self.performance
        return (c > 0) or (self.get_probability(iteration, c) > random())
