import unittest
from dxpy.web import urls


class TestUrls(unittest.TestCase):
    def test_req_url_non_suffix(self):
        result = urls.req_url('tasks', '127.0.0.1', 23300, None, 0.1, '/')
        expect = 'http://127.0.0.1:23300/api/v0.1/tasks/'

    def test_req_url_empty_base_1(self):
        result = urls.req_url('task', '127.0.0.1', 23300, 10, 0.1, '/')
        expect = 'http://127.0.0.1:23300/api/v0.1/task/10'

    def test_req_url_empty_base_2(self):
        result = urls.req_url('task', '127.0.0.1', 23300, 10, 0.1, '')
        expect = 'http://127.0.0.1:23300/api/v0.1/task/10'
        self.assertEqual(result, expect)

    def test_req_url_non_empty_base_1(self):
        result = urls.req_url('task', '127.0.0.1', 23300, 10, 0.1, '/parent')
        expect = 'http://127.0.0.1:23300/api/v0.1/parent/task/10'
        self.assertEqual(result, expect)

    def test_req_url_non_empty_base_2(self):
        result = urls.req_url('task', '127.0.0.1', 23300, 10, 0.1, 'parent')
        expect = 'http://127.0.0.1:23300/api/v0.1/parent/task/10'
        self.assertEqual(result, expect)
