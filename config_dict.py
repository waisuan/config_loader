"""
This is a custom-made/purpose dictionary class; sub-classing from Python's dict class.
Purpose:-
(1) To allow dictionaries be accessed through the dot notation and to better control the dict's query/access behaviour.
(2) To be extensible in cases where we'd want to add further/new enhancements to the class. Refer to README.md for more info on the subject.

Author: Evan Sia Wai Suan
Date created: 16/05/2019
Python Version: 3.7
"""

class ConfigDict(dict):
    def __init__(self, *args, **kwargs):
        super(ConfigDict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __getattr__(self, attr):
        # We return an empty dict here to avoid getting key errors when attempting to access a non-existant dict.
        return self.get(attr, ConfigDict())

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        super(ConfigDict, self).__setitem__(key, value)

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, "
                                "got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]
