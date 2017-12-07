import tensorflow as tf
from ...base import Net, NodeKeys
from ....model.cnn.residual import StackedResidualv2 
from dxpy.configs import configurable
from dxpy.learn.config import config
class VeryDeepDenoiseNetwork(Net):
    @configurable(config, with_name=True)
    def __init__(self, name='VDDN', inputs=None, filters=32, **kw):
        super().__init__(name, inputs, filters=stem_filters, **kw)

    def summary_items(self):
        pass

    def _make_infer(self, input_):
        ip = input_
        stem = tf.layers.conv2d(ip, self.param('filters'), 3, padding='same', name='stem')
        x = StackedResidualv2(self.name/'kernel', stem)
        resi = tf.layers.conv2d(x, 1, 3, padding='same', name='residual')
        infer = resi + ip

    def _make_loss(self, label, target):
        from dxpy.learn.model.losses import mean_square_error
        return mean_square_error(label, target)

    def _kernel(self, feeds):
        from dxpy.learn.model.image import align_crop
        from dxpy.learn.utils.general import device_name

        ip = feeds[NodeKeys.INPUT]
        infer = self._make_infer(ip)
        result = {NodeKeys.INFERENCE: infer}
        if NodeKeys.LABEL in feeds:
            loss = self._make_loss(feeds[NodeKeys.LABEL, infer]) 
            result.update(NodeKeys.LOSS: loss)
        return result
        

