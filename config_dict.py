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
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        # We return an empty dict here to avoid getting key errors when attempting to access a non-existant dict.
        return self.get(attr, ConfigDict())

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, key, value):
        super(ConfigDict, self).__setitem__(key, value)
        if isinstance( value, dict ):
            self.__dict__.update({key: ConfigDict(value)})
        else:
            self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ConfigDict, self).__delitem__(key)
        del self.__dict__[key]

    def append(self, parent, key, val):
        """
        Similar to the default behaviour of dict.update(...).
        We want to atomically allow nested dicts to be appended to our custom dict (as values).
        """
        self.__dict__[parent].update({key: val})