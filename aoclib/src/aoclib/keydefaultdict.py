from collections import defaultdict


class keydefaultdict(defaultdict):
    """A defaultdict that considers the requested key in its __missing__ function. To use, supply a default_factory
    that takes a key parameter and returns a default value for that key."""

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
