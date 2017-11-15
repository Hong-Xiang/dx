import unittest
import tensorflow as tf
import numpy as np
from dxpy.learn.model import normalizer


class TestReduceSumNormalizer(tf.test.TestCase):
    def setUp(self):
        tf.reset_default_graph()

    def tearDown(self):
        tf.reset_default_graph()

    def test_non_batch(self):
        x = np.reshape(list(range(100)), [10, 10])
        xt = tf.constant(x)
        xn = normalizer.normalizer.ReduceSum('reduce_sum',
                                             xt,
                                             fixed_sum=100.0).as_tensor()
        with self.test_session():
            pass


if __name__ == "__main__":
    tf.test.main()
