from collections import defaultdict


class keydefaultdict(defaultdict):
    """A defaultdict that considers the requested key in its default-value function"""

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
