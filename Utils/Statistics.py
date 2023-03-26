import numpy as np


class Statistics:
    def __init__(self, data):
        self.data = data

    def mean(self):
        return np.mean(self.data)

    def std(self):
        return np.std(self.data)

    def percentile(self, p):
        return np.percentile(self.data, p)

    def min(self):
        return np.min(self.data)

    def max(self):
        return np.max(self.data)

    def range(self):
        return self.max() - self.min()

    def summary(self):
        return {
            "mean": self.mean(),
            "std": self.std(),
            "percentile_25": self.percentile(25),
            "percentile_50": self.percentile(50),
            "percentile_75": self.percentile(75),
            "min": self.min(),
            "max": self.max(),
            "range": self.range()
        }
