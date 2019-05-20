import unittest
from config_loader import _is_a_group, _set_group, _set_setting
from config_dict import ConfigDict

class TestConfigLoader(unittest.TestCase):

    def test_is_a_group(self):
        result = _is_a_group('[group]')
        self.assertTrue(result is not None)

    def test_set_group(self):
        config = ConfigDict()
        group = 'group'
        result = _set_group(config, group)
        self.assertTrue(result)
        self.assertTrue(group in config)

    def test_set_setting(self):
        config = ConfigDict()
        group = 'group'
        key = 'basic_size_limit'
        value = 26214400
        _set_group(config, group)
        _set_setting(config, group, key, value)
        self.assertEqual(config.group[key], value)

if __name__ == '__main__':
    unittest.main()