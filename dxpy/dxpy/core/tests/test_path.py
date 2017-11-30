import unittest
from unittest.mock import MagicMock
from dxpy.core.path import Path


class TestPath(unittest.TestCase):
    def test_str_root(self):
        p = Path('/')
        self.assertEqual(p.abs, '/')

    def test_str_basic(self):
        p = Path('/tmp')
        self.assertEqual(p.abs, '/tmp')

    def test_parts1(self):
        p = Path('/tmp/base')
        self.assertEqual(p.parts(), ('/', 'tmp', 'base'))

    def test_parts2(self):
        p = Path('tmp/base')
        self.assertEqual(p.parts(), ('tmp', 'base'))

    def test_parent(self):
        p = Path('/tmp/base')
        self.assertEqual(p.parent(), Path('/tmp'))

    def test_name(self):
        p = Path('/tmp/base')
        self.assertEqual(p.basename, 'base')

    def test_name_dir(self):
        p = Path('/tmp/base/')
        self.assertEqual(p.basename, 'base')

    def test_copy_init(self):
        p = Path('/tmp/file')
        p2 = Path(p)
        self.assertEqual(p.abs, p2.abs)

    def test_div(self):
        p = Path('/tmp')
        p = p / 'sub'
        self.assertEqual(p.abs, '/tmp/sub')

    def test_tilde_support(self):
        p = Path('~/x')
        import os
        self.assertEqual(str(p), os.environ['HOME']+'/x')

    def test_mid_tilde_support(self):
        p = Path('a/x~y')
        self.assertEqual(str(p), 'a/x~y')
