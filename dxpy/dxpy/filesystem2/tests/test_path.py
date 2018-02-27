import unittest
from unittest.mock import MagicMock
from dxpy.filesystem2.path import Path


def subtests(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    for i, args in enumerate(zip(inputs, outputs)):
        with tc.subTest(i + offset):
            func(*args)


def subtests_ae(tc: unittest.TestCase, inputs, outputs, func, offset=0):
    subtests(tc, inputs, outputs,
             lambda xi, xo: tc.assertEqual(func(xi), xo), offset)


class TestPath(unittest.TestCase):
    def test_s(self):
        inputs = ['/', '/tmp', '%2Ftmp', '%252Ftmp', './tmp', '/tmp/a/..']
        outputs = ['/', '/tmp', '/tmp', '/tmp', 'tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).s)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).raw, len(inputs))

    def test_absolute_and_a(self):
        inputs = ['/', 'tmp', '/tmp']
        outputs = ['/', '/tmp', '/tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).a)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).absolute().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).absolute(),
                                                      Path),
                 len(inputs) * 2)

    def test_relative(self):
        inputs = ['/', 'tmp', '/tmp', '/tmp/']
        outputs = ['', 'tmp', 'tmp', 'tmp']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).r)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).relative().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).relative(),
                                                      Path),
                 len(inputs) * 2)

    def test_name_and_n(self):
        inputs = ['/', 'a', '/a/b', '/a/b/']
        outputs = ['', 'a', 'b', 'b']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).n)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).name().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).name(), Path),
                 len(inputs) * 2)

    def test_parts(self):
        with self.subTest(0):
            p = Path('/tmp/base')
            self.assertEqual(p.parts(), ('/', 'tmp', 'base'))
        with self.subTest(1):
            p = Path('a/b')
            self.assertEqual(p.parts(), ('a', 'b'))

    def test_father_and_f(self):
        inputs = ['a/b', '/a/b', '/a/b/', 'a/b/']
        outputs = ['a', '/a', '/a', 'a']
        subtests_ae(self, inputs, outputs, lambda x: Path(x).f)
        subtests_ae(self, inputs, outputs, lambda x: Path(x).father().s,
                    len(inputs))
        subtests(self, inputs, outputs,
                 lambda xi, xo: self.assertIsInstance(Path(xi).father(), Path),
                 len(inputs) * 2)

    def test_div(self):
        with self.subTest(0):
            p = Path('/tmp')
            p = p / 'sub'
            self.assertEqual(p.s, '/tmp/sub')
        with self.subTest(1):
            p = Path('/tmp')
            p = p / 'sub/'
            self.assertEqual(p.s, '/tmp/sub')

    def test_eq(self):
        ips = ['a', 'a/b', '/a/b', './a', '/a/b/c/..']
        ops = ['a', 'a/b', '/a/b', './a', '/a/b']
        subtests(self, ips, ops,
                 lambda xi, xo: self.assertTrue(Path(xi) == Path(xo)))
