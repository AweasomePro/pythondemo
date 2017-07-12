try:
    import typing # python3.5
    from typing import cast
    _ObjectDictBase = typing.Dict[str,typing.Any]
except ImportError:
    _ObjectDictBase = dict
    def cast(typ, x):
        return x


class ObjectDict(_ObjectDictBase):
    """
    Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
