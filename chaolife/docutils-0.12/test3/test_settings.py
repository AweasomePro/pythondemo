#!/usr/bin/env python

# $Id: test_settings.py 7630 2013-03-15 22:27:04Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests of runtime settings.
"""

import sys
import os
import difflib
import pprint
import warnings
import unittest
import DocutilsTestSupport              # must be imported before docutils
from docutils import frontend, utils
from docutils.writers import html4css1, pep_html
from docutils.parsers import rst


warnings.filterwarnings(action='ignore',
                        category=frontend.ConfigDeprecationWarning)


def fixpath(path):
    return os.path.abspath(os.path.join(*(path.split('/'))))


class ConfigFileTests(unittest.TestCase):

    config_files = {'old': fixpath('data/config_old.txt'),
                    'one': fixpath('data/config_1.txt'),
                    'two': fixpath('data/config_2.txt'),
                    'list': fixpath('data/config_list.txt'),
                    'list2': fixpath('data/config_list_2.txt'),
                    'error': fixpath('data/config_error_handler.txt')}

    settings = {
        'old': {'datestamp': '%Y-%m-%d %H:%M UTC',
                'generator': True,
                'no_random': True,
                'python_home': 'http://www.python.org',
                'source_link': True,
                'stylesheet': None,
                'stylesheet_path': ['stylesheets/pep.css'],
                'template': fixpath('data/pep-html-template')},
        'one': {'datestamp': '%Y-%m-%d %H:%M UTC',
                'generator': True,
                'no_random': True,
                'python_home': 'http://www.python.org',
                'raw_enabled': False,
                'record_dependencies': utils.DependencyList(),
                'source_link': True,
                'stylesheet': None,
                'stylesheet_path': ['stylesheets/pep.css'],
                'tab_width': 8,
                'template': fixpath('data/pep-html-template'),
                'trim_footnote_reference_space': True,
               },
        'two': {'footnote_references': 'superscript',
                'generator': False,
                'record_dependencies': utils.DependencyList(),
                'stylesheet': None,
                'stylesheet_path': ['test.css'],
                'trim_footnote_reference_space': None},
        'list': {'expose_internals': ['a', 'b', 'c', 'd', 'e'],
                 'strip_classes': ['spam', 'pan', 'fun', 'parrot'],
                 'strip_elements_with_classes': ['sugar', 'flour', 'milk',
                                                  'safran']},
        'list2': {'expose_internals': ['a', 'b', 'c', 'd', 'e', 'f'],
                  'strip_classes': ['spam', 'pan', 'fun', 'parrot',
                                     'ham', 'eggs'],
                  'strip_elements_with_classes': ['sugar', 'flour',
                                                   'milk', 'safran',
                                                   'eggs', 'salt']},
        'error': {'error_encoding': 'ascii',
                  'error_encoding_error_handler': 'strict'},
        }

    compare = difflib.Differ().compare
    """Comparison method shared by all tests."""

    def setUp(self):
        self.option_parser = frontend.OptionParser(
            components=(pep_html.Writer, rst.Parser), read_config_files=None)

    def files_settings(self, *names):
        settings = frontend.Values()
        for name in names:
            settings.update(self.option_parser.get_config_file_settings(
                self.config_files[name]), self.option_parser)
        return settings.__dict__

    def expected_settings(self, *names):
        expected = {}
        for name in names:
            expected.update(self.settings[name])
        return expected

    def compare_output(self, result, expected):
        """`result` and `expected` should both be dicts."""
        self.assertTrue('record_dependencies' in result)
        if 'record_dependencies' not in expected:
            # Delete it if we don't want to test it.
            del result['record_dependencies']
        result = pprint.pformat(result) + '\n'
        expected = pprint.pformat(expected) + '\n'
        try:
            self.assertEqual(result, expected)
        except AssertionError:
            print('\n%s\n' % (self,), file=sys.stderr)
            print('-: expected\n+: result', file=sys.stderr)
            print(''.join(self.compare(expected.splitlines(1),
                                                     result.splitlines(1))), file=sys.stderr)
            raise

    def test_nofiles(self):
        self.compare_output(self.files_settings(),
                            self.expected_settings())

    def test_old(self):
        self.compare_output(self.files_settings('old'),
                            self.expected_settings('old'))

    def test_one(self):
        self.compare_output(self.files_settings('one'),
                            self.expected_settings('one'))

    def test_multiple(self):
        self.compare_output(self.files_settings('one', 'two'),
                            self.expected_settings('one', 'two'))

    def test_old_and_new(self):
        self.compare_output(self.files_settings('old', 'two'),
                            self.expected_settings('old', 'two'))

    def test_list(self):
        self.compare_output(self.files_settings('list'),
                            self.expected_settings('list'))

    def test_list2(self):
        self.compare_output(self.files_settings('list', 'list2'),
                            self.expected_settings('list2'))

    def test_error_handler(self):
        self.compare_output(self.files_settings('error'),
                            self.expected_settings('error'))


class ConfigEnvVarFileTests(ConfigFileTests):

    """
    Repeats the tests of `ConfigFileTests` using the ``DOCUTILSCONFIG``
    environment variable and the standard Docutils config file mechanism.
    """

    def setUp(self):
        ConfigFileTests.setUp(self)
        self.orig_environ = os.environ
        os.environ = os.environ.copy()

    def files_settings(self, *names):
        files = [self.config_files[name] for name in names]
        os.environ['DOCUTILSCONFIG'] = os.pathsep.join(files)
        settings = self.option_parser.get_standard_config_settings()
        return settings.__dict__

    def tearDown(self):
        os.environ = self.orig_environ


class HelperFunctionsTests(unittest.TestCase):

    pathdict = {'foo': 'hallo', 'ham': 'h\xE4m', 'spam': 'spam'}
    keys = ['foo', 'ham']

    def test_make_paths_absolute(self):
        pathdict = self.pathdict.copy()
        frontend.make_paths_absolute(pathdict, self.keys, base_path='base')
        self.assertEqual(pathdict['foo'], os.path.abspath('base/hallo'))
        self.assertEqual(pathdict['ham'], os.path.abspath('base/h\xE4m'))
        # not touched, because key not in keys:
        self.assertEqual(pathdict['spam'], 'spam')

    def test_make_paths_absolute_cwd(self):
        # With base_path None, the cwd is used as base path.
        # Settings values may-be `unicode` instances, therefore
        # os.getcwdu() is used and the converted path is a unicode instance:
        pathdict = self.pathdict.copy()
        frontend.make_paths_absolute(pathdict, self.keys)
        self.assertEqual(pathdict['foo'], os.path.abspath('hallo'))
        self.assertEqual(pathdict['ham'], os.path.abspath('h\xE4m'))
        # not touched, because key not in keys:
        self.assertEqual(pathdict['spam'], 'spam')

    def test_validate_colon_separated_string_list(self):
        tests = (
                    ('a', ['a',] ),
                    ('a', ['a',] ),
                    ('a:b', ['a', 'b'] ),
                    ('a:b', ['a', 'b'] ),
                    (['a',], ['a',] ),
                    (['a', 'b:c'], ['a', 'b', 'c'] ),
                )
        for t in tests:
            self.assertEqual(
                    frontend.validate_colon_separated_string_list(None, t[0], None),
                    t[1])


    def test_validate_comma_separated_list(self):
        tests = (
                    ('a', ['a',] ),
                    ('a', ['a',] ),
                    ('a,b', ['a', 'b'] ),
                    ('a,b', ['a', 'b'] ),
                    (['a',], ['a',] ),
                    (['a', 'b,c'], ['a', 'b', 'c'] ),
                    (['a', 'b,c'], ['a', 'b', 'c'] ),
                )
        for t in tests:
            self.assertEqual(
                    frontend.validate_comma_separated_list(None, t[0], None),
                    t[1])

if __name__ == '__main__':
    unittest.main()
