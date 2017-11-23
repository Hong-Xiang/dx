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

    def summary_items(self):
        from ...train.summary import SummaryItem
        from ...scalar import global_step
        result = {
            'loss':     SummaryItem(self.nodes[NodeKeys.EVALUATE]),
            'global_step': SummaryItem(global_step())}
        for i in range(1, self.param('nb_down_sample') + 1):
            result.update({'img{}x'.format(2**i):
                           SummaryItem(self.nodes['input/image{}x'.format(2**i)])})
        for i in range(self.param('nb_down_sample')):
            result.update({'lab{}x'.format(2**i):
                           SummaryItem(self.nodes['label/image{}x'.format(2**i)])})
        result.update({'inf': SummaryItem(self.nodes[NodeKeys.INFERENCE])})
        return result
        # def _get_node(self, node_type, down_sample_ratio, source=None):
        #     if source is None:
        #         source = self.nodes
        #     name = "{}/image{}x".format(node_type, 2**down_sample_ratio)
        #     return source[name]

    def _post_kernel_post_outputs(self):
        self.register_node(NodeKeys.EVALUATE,
                           self.nodes['outputs/{}'.format(NodeKeys.EVALUATE)])
        super()._post_kernel_post_outputs()

    def _kernel(self, feeds):
        from ...model.cnn.super_resolution import SuperResolutionMultiScale
        from ...model.tensor import MultiGPUSplitor, PlaceHolder
        from ...utils.general import device_name
        from dxpy.collections.dicts import swap_dict_hierarchy
        mgs = MultiGPUSplitor(nb_gpu=self.param('nb_gpu'))
        feeds_gpus = mgs(feeds)
        first_part = list(feeds_gpus.values())[0]
        with tf.name_scope('cpu_placeholders'):
            cpu_placeholders = {k: PlaceHolder(
                first_part[k]).as_tensor() for k in first_part}
        with tf.device(device_name('cpu')):
            model = SuperResolutionMultiScale('model', cpu_placeholders,
                                              self.param('nb_down_sample'))
            model()
        result_gpus = {}
        for i, k in enumerate(mgs.part_names()):
            with tf.device(device_name('gpu', i)):
                result_gpus[k] = model(feeds_gpus[k])
        with tf.device(device_name('cpu')):
            with tf.name_scope('merge'):
                with tf.name_scope('inference'):
                    infer = tf.concat([result_gpus[k][NodeKeys.INFERENCE]
                                       for k in mgs.part_names()], axis=0)
                losses = [result_gpus[k][NodeKeys.LOSS]
                          for k in mgs.part_names()]
                with tf.name_scope('total_loss'):
                    loss = tf.add_n(losses)
                # tf.placeholder(tf.float32, [], name='dummpyPH')
        return {NodeKeys.INFERENCE: infer,
                NodeKeys.LOSS: losses,
                NodeKeys.EVALUATE: loss}

    # def _kernel_multiscale(self, image_lowest, image_labels):
    #     """
    #     Returns:
    #         images_infer, cropped inferenced images (different scale)
    #         loss (total loss)
    #     """
    #     rep = None
    #     ipt = image_lowest
    #     losses = []
    #     for i in reversed(range(self.param(nb_down_sample))):
    #         with tf.variable_scope('sr2x_{}'.format(i)):
    #             ipt, loss, rep = self._kernel_sr2x(ipt, image_labels[i], rep,
    #                                                name='srb_{}'.format(i))
    #             losses.append(loss * ((0.5)**i))
    #     with tf.name_scope("loss"):
    #         loss = tf.add_n(losses)
    #     return ipt, loss
