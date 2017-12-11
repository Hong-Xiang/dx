import tensorflow as tf
from ...base import Net, Graph, NodeKeys
from ....model.cnn.super_resolution import SuperResolutionMultiScalev2, SRKeys


class SRNetKeys:
    RES_INF = 'res_inf'
    RES_ITP = 'res_itp'
    LOSS_ITP = 'loss_itp'


from dxpy.configs import configurable
from ....config import config

# class SRMultiScale(Net):
#     """
#     Required inputs:
#     'input/image2x'|...|'input/image8x'
#     'label/image1x', ..., 'label/image4x'
#     """
#     @configurable(config, with_name=True)
#     def __init__(self, inputs, name='network', nb_gpu=2, nb_down_sample=3, **kw):
#         super().__init__(name, inputs, nb_gpu=nb_gpu, nb_down_sample=nb_down_sample, **kw)


#     def summary_items(self):
#         from ....train.summary import SummaryItem
#         from ....scalar import global_step
#         result = {
#             'loss':     SummaryItem(self.nodes[NodeKeys.EVALUATE]),
#             'global_step': SummaryItem(global_step())}
#         max_down_sample = self.param('nb_down_sample')
#         result.update({'img{}x'.format(2**max_down_sample):
#                        SummaryItem(self.nodes['input/image{}x'.format(2**max_down_sample)])})
#         result.update({'inf': SummaryItem(self.nodes[NodeKeys.INFERENCE])})
#         result.update(
#             {'itp': SummaryItem(self.nodes['outputs/{}'.format(SRKeys.INTERP)])})
#         result.update({'label': SummaryItem(
#             self.nodes['outputs/{}'.format(SRKeys.ALIGNED_LABEL)])})
#         result.update({'res_inf': SummaryItem(
#             self.nodes['outputs/{}'.format(SRNetKeys.RES_INF)])})
#         result.update({'res_itp': SummaryItem(
#             self.nodes['outputs/{}'.format(SRNetKeys.RES_ITP)])})

#         if 'outputs/'+SRKeys.POI_LOSS in self.nodes is not None:
#             result.update({'poi_loss': SummaryItem(self.noddes['outputs/'+SRKeys.POI_LOSS])})
#             result.update({'mse_loss': SummaryItem(self.noddes['outputs/'+SRKeys.MSE_LOSS])})
#         return result
#         # def _get_node(self, node_type, down_sample_ratio, source=None):
#         #     if source is None:
#         #         source = self.nodes
#         #     name = "{}/image{}x".format(node_type, 2**down_sample_ratio)
#         #     return source[name]

#     def _post_kernel_post_outputs(self):
#         self.register_node(NodeKeys.EVALUATE,
#                            self.nodes['outputs/{}'.format(NodeKeys.EVALUATE)])
#         super()._post_kernel_post_outputs()

#     def _kernel(self, feeds):

#         from ....model.tensor import MultiGPUSplitor, PlaceHolder
#         from ....utils.general import device_name
#         from ....model.image import align_crop
#         from dxpy.collections.dicts import swap_dict_hierarchy
#         mgs = MultiGPUSplitor(nb_gpu=self.param('nb_gpu'))
#         feeds_gpus = mgs(feeds)
#         first_part = list(feeds_gpus.values())[0]
#         with tf.name_scope('cpu_placeholders'):
#             cpu_placeholders = {k: PlaceHolder(
#                 first_part[k]).as_tensor() for k in first_part}
#         with tf.device(device_name('cpu')):
#             model = SuperResolutionMultiScalev2(name='model', inputs=cpu_placeholders)
#             model()
#         result_gpus = {}
#         for i, k in enumerate(mgs.part_names()):
#             with tf.device(device_name('gpu', i)):
#                 result_gpus[k] = model(feeds_gpus[k])
#         with tf.device(device_name('cpu')):
#             with tf.name_scope('merge'):
#                 with tf.name_scope('inference'):
#                     infer = tf.concat([result_gpus[k][NodeKeys.INFERENCE]
#                                        for k in mgs.part_names()], axis=0)
#                 with tf.name_scope('label'):
#                     label = tf.concat([result_gpus[k][SRKeys.ALIGNED_LABEL]
#                                        for k in mgs.part_names()], axis=0)
#                 with tf.name_scope('interp'):
#                     interp = tf.concat([result_gpus[k][SRKeys.INTERP]
#                                         for k in mgs.part_names()], axis=0)
#                 with tf.name_scope('residual'):
#                     res_inf = tf.abs(label - infer)
#                     res_itp = tf.abs(label - interp)
#                 losses = [result_gpus[k][NodeKeys.LOSS]
#                           for k in mgs.part_names()]
#                 if SRKeys.POI_LOSS in result_gpus[mgs.part_names()[0]]:
#                     losses_poi = [result_gpus[k][SRKeys.POI_LOSS]
#                                   for k in mgs.part_names()]
#                     losses_mse = [result_gpus[k][SRKeys.MSE_LOSS]
#                                   for k in mgs.part_names()]
#                 else:
#                     losses_poi = None
#                     losses_mse = None

#                 with tf.name_scope('total_loss'):
#                     loss = tf.add_n(losses)
#                     if losses_poi is not None:
#                         loss_poi = tf.add_n(losses_poi)
#                         loss_mse = tf.add_n(losses_mse)
#                     else:
#                         loss_poi = None
#                         loss_mse = None

#         result = {NodeKeys.INFERENCE: infer,
#                   SRKeys.ALIGNED_LABEL: label,
#                   SRKeys.INTERP: interp,
#                   SRNetKeys.RES_INF: res_inf,
#                   SRNetKeys.RES_ITP: res_itp,
#                   NodeKeys.LOSS: losses,
#                   NodeKeys.EVALUATE: loss}
#         if loss_poi is not None:
#             result.update({SRKeys.MSE_LOSS: loss_mse,
#                            SRKeys.POI_LOSS: loss_poi})
#         return result

class SRMultiScale(Net):
    """
    Required inputs:
    'input/image2x'|...|'input/image8x'
    'label/image1x', ..., 'label/image4x'
    """
    @configurable(config, with_name=True)
    def __init__(self, inputs, name='network', nb_gpu=2, nb_down_sample=3, **kw):
        super().__init__(name, inputs, nb_gpu=nb_gpu, nb_down_sample=nb_down_sample, **kw)

    def summary_items(self):
        from ....train.summary import SummaryItem
        from ....scalar import global_step
        result = {'loss':     SummaryItem(self.nodes[NodeKeys.EVALUATE])}
        result.update{'loss_itp': SummaryItem(self.nodes['outputs/{}'.format(SRNetKeys.LOSS_ITP)])}
        max_down_sample = self.param('nb_down_sample')
        result.update({'img{}x'.format(2**max_down_sample):
                       SummaryItem(self.nodes['input/image{}x'.format(2**max_down_sample)])})
        result.update({'inf': SummaryItem(self.nodes[NodeKeys.INFERENCE])})
        result.update(
            {'itp': SummaryItem(self.nodes['outputs/{}'.format(SRKeys.INTERP)])})
        result.update({'label': SummaryItem(
            self.nodes['outputs/{}'.format(SRKeys.ALIGNED_LABEL)])})
        result.update({'res_inf': SummaryItem(
            self.nodes['outputs/{}'.format(SRNetKeys.RES_INF)])})
        result.update({'res_itp': SummaryItem(
            self.nodes['outputs/{}'.format(SRNetKeys.RES_ITP)])})

        if 'outputs/' + SRKeys.POI_LOSS in self.nodes is not None:
            result.update({'poi_loss': SummaryItem(
                self.noddes['outputs/' + SRKeys.POI_LOSS])})
            result.update({'mse_loss': SummaryItem(
                self.noddes['outputs/' + SRKeys.MSE_LOSS])})
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
        from ....model.tensor import MultiGPUSplitor, PlaceHolder
        from ....utils.general import device_name
        from ....model.image import align_crop
        from dxpy.learn.model.losses import mean_square_error
        from dxpy.collections.dicts import swap_dict_hierarchy
        result = SuperResolutionMultiScalev2(name='model', inputs=feeds)()
        with tf.name_scope('residuals'):
            res_inf = tf.abs(
                result[SRKeys.ALIGNED_LABEL] - result[NodeKeys.INFERENCE])
            res_itp = tf.abs(
                result[SRKeys.ALIGNED_LABEL] - result[SRKeys.INTERP])
        if NodeKeys.LOSS in result:
            loss_itp = mean_square_error(result[SRKeys.ALIGNED_LABEL], result[SRKeys.INTERP])
            result.update({SRNetKeys.LOSS_ITP: loss_itp})
        result.update({SRNetKeys.RES_INF: res_inf})
        result.update({SRNetKeys.RES_ITP: res_inf})
        result.update({NodeKeys.EVALUATE: result[NodeKeys.LOSS]})
        return result
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
