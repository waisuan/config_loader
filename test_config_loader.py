import unittest
from config_loader import _is_a_group, _is_standard_setting, _is_override_setting, _set_group, _set_setting, _set_override_setting
from config_dict import ConfigDict

class TestConfigLoader(unittest.TestCase):

    def test_is_a_group(self):
        result = _is_a_group('[group]')
        self.assertTrue(result is not None)

    def test_is_standard_setting(self):
        result = _is_standard_setting('student_size_limit = 52428800')
        self.assertTrue(result is not None)

    def test_is_override_setting(self):
        result = _is_override_setting('path<production> = /srv/var/tmp/')
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

    def test_set_override_setting(self):
        config = ConfigDict()
        group = 'group'
        key = 'path'
        override = 'production'
        value = '/srv/var/tmp/'
        _set_group(config, group)
        _set_override_setting(config, group, [key,override,value], ['production'])
        self.assertEqual(config.group[key], value)

if __name__ == '__main__':
    unittest.main()
