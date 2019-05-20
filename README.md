Author: Evan Sia Wai Suan
Environment/language: Python 3.7

Contents:-
(1) config_loader.py - A module containing the `load_config()` function. It can be used directly as-is or imported as a separate helper module.
(2) config_dict.py - A custom-made/purpose dictionary class created specifically for this assignment.

How to execute code?
(1) python config_loader.py --config_file=<CONFIG FILE PATH/NAME>
(2) >>> python
    >>> from config_loader import load_config
    >>> config = load_config(<CONFIG FILE PATH/NAME>, [<OVERRIDE_1, OVERRIDE_2, ...>])
    >>> config.<KEY>

Notes:-
- Due to the varying size of the input config file, I opted to not load the file all at once into memory and resorted to reading/parsing it one line at a time. This gave me the control to skip over any unnecessary lines (e.g. comments) and only keep what was necessary.
- I used regex to help identify the correct line patterns and due to how expensive regex can be, I halt all (unnecessary) regex searches once a pattern has been found.
- Using a dictionary data structure allowed the querying of the parsed config object to  take a constant amount of time. Additionally, it was easier to parse the config file into a dict-like object due to the nature of the file's contents being in the form of key-value pairs.
- I opted to create a custom dictionary class (wrapping around Python's dict module) in order to allow better control over how the object can/should be queried after it has been returned to the caller. E.g. accessing values through the dot notation && returning an empty object if/when a key does not exist under the config object.
- I've kept all private/helper functions under `config_loader.py` as cohesive, lightweight, and unit-testable as possible as well as have the `load_config()` function be short and simple enough to follow/maintain by future devs.
- I've added comments and docs around functions/LoC that I deemed necessary in order to allow future maintainers to understand the codebase easier/quicker.

Future enhancement(s):-
- Add LRU feature/functionality to the `ConfigDict` class.
    - If cache/memory size is a concern, we can restrict the dictionary to a strict size of N keys and be able to remove/pop the least recently used key-value pair off of the dict whenever we exceed its size and need to append the most recently used / new key-value pair to it. The only downside to this is that we _may_ need to re-parse & re-fetch from the config file if a key does not currently exist within the dict -- which may impact the overall query time. We may be able to see less fetches from disk/file if our dict is large enough to hold a high no. of the most-recently used key-val pairs. Picking an optimal dict size would prove to be an important factor in the overall design & implementation here.
   - Pre-loading the dict with a strict amount of key-val pairs can help speed up boost time as well since we won't have to go through and parse the entire file during that time.