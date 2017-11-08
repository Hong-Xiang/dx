import unittest
import rx
from fs.memoryfs import MemoryFS
from dxpy import batch
# from dxpy import batch


class TestFilesFilter(unittest.TestCase):
    def setUp(self):
        self.fs = MemoryFS()
        for i in range(5):
            self.fs.makedir('sub.{0}'.format(i))
            with self.fs.opendir('sub.{0}'.format(i)) as d:
                d.touch('result.txt')
        for i in range(5):
            self.fs.makedir('child.{0}'.format(i))
            with self.fs.opendir('child.{0}'.format(i)) as d:
                d.touch('result.txt')
        for i in range(5):
            self.fs.touch('result.{}.txt'.format(i))
            self.fs.touch('errors.{}.txt'.format(i))

    def tearDown(self):
        self.fs.close()

    def test_basic(self):
        ff = batch.FilesFilter(include_filters=['result*'])
        results = set(ff.lst(self.fs))
        expected = {'result.{}.txt'.format(i) for i in range(5)}
        self.assertEqual(results, expected)

    def test_multi_filters(self):
        ff = batch.FilesFilter(include_filters=['result*', 'errors*'])
        results = set(ff.lst(self.fs))
        expected = {'result.{}.txt'.format(i) for i in range(
            5)}.union({'errors.{}.txt'.format(i) for i in range(5)})
        self.assertEqual(results, expected)

    def test_with_directory_filter(self):
        results = set()
        (batch.DirectoriesFilter(['sub*']).obv(self.fs)
         .flat_map(lambda p: batch.FilesFilter(['result*']).obv(self.fs, p))
         .subscribe(results.add))
        expected = {'sub.{}/result.txt'.format(i) for i in range(5)}
        self.assertEqual(results, expected)


class DirectoriesFilter(unittest.TestCase):
    def setUp(self):
        self.fs = MemoryFS()
        for i in range(5):
            self.fs.makedir('sub.{0}'.format(i))
            with self.fs.opendir('sub.{0}'.format(i)) as d:
                d.makedir('sub.0')
        for i in range(5):
            self.fs.makedir('child.{0}'.format(i))

    def tearDown(self):
        self.fs.close()

    def test_basic(self):
        ff = batch.DirectoriesFilter(include_filters=['sub*'])
        results = set(ff.lst(self.fs))
        expected = {'sub.{}'.format(i) for i in range(5)}
        self.assertEqual(results, expected)

    def test_depth_1(self):
        ff = batch.DirectoriesFilter(include_filters=['sub*'], depth=1)
        results = set(ff.lst(self.fs))
        expected = {'sub.{}'.format(i) for i in range(
            5)}.union({'sub.{}/sub.0'.format(i) for i in range(5)})
        self.assertEqual(results, expected)
