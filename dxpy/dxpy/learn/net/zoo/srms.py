import tensorflow as tf
from ..base import Net, Graph, NodeKeys
from ...model.image import resize
from ...model.cnn.blocks import StackedConv2D


def sr_end(res, itp, ip_h, name='sr_end', is_res=True):
    """ Assuming shape(itp) == shape(ip_h)
    reps is center croped shape of itp/ip_h
    """
    with tf.name_scope(name):
        spo = res.shape.as_list()[1:3]
        spi = itp.shape.as_list()[1:3]
        cpx = (spi[0] - spo[0]) // 2
        cpy = (spi[1] - spo[1]) // 2
        crop_size = (cpx, cpy)
        itp_c = Cropping2D(crop_size)(itp)
        with tf.name_scope('output'):
            inf = add([res, itp_c])
        if is_res:
            with tf.name_scope('label_cropped'):
                ip_c = Cropping2D(crop_size)(ip_h)
            with tf.name_scope('res_out'):
                res_inf = sub(ip_c, inf)
            with tf.name_scope('res_itp'):
                res_itp = sub(ip_c, itp_c)
        else:
            res_inf = None
            res_itp = None
        return (inf, crop_size, res_inf, res_itp)


class SRMultiScale(Net):
    """
    Required inputs:
    'input/image2x'|...|'input/image8x'
    'label/image1x', ..., 'label/image4x'
    """

    def __init__(self, inputs, name='network', **config):
        super().__init__(name, inputs, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'nb_gpu': 2,
            'nb_down_sample': 3,
        }, super()._default_config())

    def _get_node(self, node_type, down_sample_ratio, source=None):
        if source is None:
            source = self.nodes
        name = "{}/image{}x".format(node_type, 2**down_sample_ratio)
        return source[name]

    def _kernel(self, feeds):
        x = None
        for i_down_sample in reversed(range(self.param('nb_down_sample'))):
            if x is None:
                x = self._get_node('input', i_down_sample)
                u = resize(x, (2, 2))

        with tf.name_scope('inference'):
            y = tf.layers.conv2d(h, 1, 3, padding='same')
        result = {NodeKeys.INFERENCE: y}
        if NodeKeys.LABEL in feeds:
            with tf.name_scope('loss'):
                l = tf.losses.mean_squared_error(feeds[NodeKeys.LABEL], y)
        result[NodeKeys.LOSS] = l
        return result

    def _kernel_multiscale(self, image_lowest, image_labels):
        """
        Returns:
            images_infer, cropped inferenced images (different scale)
            loss (total loss)
        """
        rep = None
        ipt = image_lowest
        losses = []
        for i in reversed(range(self.param(nb_down_sample))):
            with tf.variable_scope('sr2x_{}'.format(i)):
                ipt, loss, rep = self._kernel_sr2x(ipt, image_labels[i], rep,
                                                   name='srb_{}'.format(i))
                losses.append(loss * ((0.5)**i))
        with tf.name_scope("loss"):
            loss = tf.add_n(losses)
        return ipt, loss

