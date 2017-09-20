import unittest
import datetime
from dxpy.time.timestamps import Start, Duration, Run, Progress


class TestStart(unittest.TestCase):
    def test_init_basic(self):
        start = datetime.datetime.utcnow()
        ts = Start(start=start)
        self.assertEqual(start, ts.start)


class TestDuration(unittest.TestCase):
    def test_init_basic(self):
        start = datetime.datetime.utcnow()
        end = start + datetime.timedelta(seconds=10)
        td = Duration(start=start, end=end)
        self.assertEqual(start, td.start)
        self.assertEqual(end, td.end)

    def test_length(self):
        start = datetime.datetime.utcnow()
        delta = datetime.timedelta(seconds=10)
        end = start + delta
        td = Duration(start=start, end=end)
        self.assertEqual(delta, td.length)


class TestRun(unittest.TestCase):
    def test_init_basic(self):
        start = datetime.datetime.utcnow()
        run = datetime.timedelta(seconds=10)
        tr = Run(start=start, run=run)
        self.assertEqual(start, tr.start)
        self.assertEqual(run, tr.run)

    def test_init_no_run(self):
        start = datetime.datetime.utcnow()
        tr = Run(start=start)
        self.assertEqual(datetime.timedelta(), tr.run)

    def test_update_run(self):
        start = datetime.datetime.utcnow()
        tr = Run(start=start)
        tr.update_run()


class TestProgress(unittest.TestCase):
    def test_init_basic(self):
        start = datetime.datetime.utcnow()
        delta_all = datetime.timedelta(seconds=10)
        end = start + delta_all
        delta_run = datetime.timedelta(seconds=5)
        run = start + delta_run
        tp = Progress(start=start, end=end, run=run)
        self.assertEqual(start, tp.start)
        self.assertEqual(end, tp.end)
        self.assertEqual(run, tp.run)

    def test_progress(self):
        start = datetime.datetime.utcnow()
        delta_all = datetime.timedelta(seconds=10)
        end = start + delta_all
        delta_run = datetime.timedelta(seconds=5)
        tp = Progress(start=start, end=end, run=delta_run)
        self.assertAlmostEqual(0.5, tp.progress)

    def test_update_end(self):
        start = datetime.datetime.utcnow()
        delta_all = datetime.timedelta(seconds=10)
        end = start + delta_all
        delta_run = datetime.timedelta(seconds=5)
        tp = Progress(start=start, end=end, run=delta_run)
        end_new = start + datetime.timedelta(seconds=20)
        tp.update_end(end_new)
        self.assertEqual(end_new, tp.end)


if __name__ == "__main__":
    unittest.main()
