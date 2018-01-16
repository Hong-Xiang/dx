import unittest
import numpy as np
from ..io.visual import _unified_images


class TestUnifiedImages(unittest.TestCase):
    def test_one_dimension(self):
        data = np.ones([64] * 2)
        images = [data, None]
        images = _unified_images(images)
        self.assertEqual(images.shape, (1, 2))

    def test_multi_dimension_gray(self):
        datas = [np.ones([2, 3, 64, 64]),
                 np.ones([2, 3, 1, 64, 64]),
                 np.ones([2, 3, 1, 64, 64, 1]),
                 np.ones([2, 3, 64, 64, 1]),
                 ]
        images = [_unified_images(d) for d in datas]
        for i, im in enumerate(images):
            self.assertEqual(im.shape, (2, 3))
            self.assertEqual(im[0, 0].shape, (64, 64))

    def test_multi_dimension_rgb(self):
        datas = [np.ones([2, 3, 64, 64, 3]),
                 np.ones([2, 3, 1, 64, 64, 3]),
                 ]
        images = [_unified_images(d) for d in datas]
        for i, im in enumerate(images):
            self.assertEqual(im.shape, (2, 3))
            self.assertEqual(im[0, 0].shape, (64, 64, 3))

    def test_multi_shape(self):
        img1 = np.ones([64, 64])
        img2 = np.ones([128, 128])
        imgs = _unified_images([img1, img2])
        self.assertEqual(imgs.shape, (1, 2))
        self.assertEqual(imgs[0, 0].shape, (64, 64))
        self.assertEqual(imgs[0, 1].shape, (128, 128))
