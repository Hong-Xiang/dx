import tensorflow as tf
from ..base import Model, NodeKeys
from .blocks import StackedConv2D, ResidualStackedConv
from ..image import align_crop


class SRKeys:
    REPRESENTS = 'reps'
    RESIDUAL = 'resi'
    ALIGNED_LABEL = 'aligned_label'


class BuildingBlocks:
    STACKEDCONV = 'stacked_conv'
    RESCONV2 = 'res_conv_2'
    RESINCEPT = 'res_incept'


class SuperResolution2x(Model):
    def __init__(self, name, inputs, building_block=None, **config):
        super().__init__(name, inputs, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'building_block': BuildingBlocks.STACKEDCONV,
            'nb_layers': 10,
            'filters': 32,
            'boundary_crop': [0, 0]
        }, super()._default_config())

    def _kernel(self, feeds):
        from ..image import resize, boundary_crop
        with tf.name_scope('input'):
            u = resize(feeds[NodeKeys.INPUT], (2, 2))
            if SRKeys.REPRESENTS in feeds:
                r = resize(feeds[SRKeys.REPRESENTS], (2, 2))
                r = tf.concat([r, u], axis=3)
            else:
                r = u
        if self.param('building_block') == BuildingBlocks.STACKEDCONV:
            x = StackedConv2D('kernel', u,
                              nb_layers=self.param('nb_layers'),
                              filters=self.param('filters'))()
        elif self.param('building_block') == BuildingBlocks.RESCONV2:
            x = u
            with tf.variable_scope('kernel'):
                for i in range(self.param('nb_layers')):
                    x = ResidualStackedConv(
                        self.name / 'res_{}'.format(i), x)()
        with tf.variable_scope('inference'):
            res = tf.layers.conv2d(x, 1, 3, padding='same')
            res = boundary_crop(res, self.param('boundary_crop'))
            u_c = align_crop(u, res)
            y = res + u_c
        result = {NodeKeys.INFERENCE: y,
                  SRKeys.REPRESENTS: x,
                  SRKeys.RESIDUAL: res}
        if NodeKeys.LABEL in feeds:
            with tf.name_scope('loss'):
                aligned_label = align_crop(feeds[NodeKeys.LABEL], y)
                l = tf.losses.mean_squared_error(aligned_label, y)
            result.update({NodeKeys.LOSS: l})
        return result


class SuperResolutionMultiScale(Model):
    def __init__(self, name, inputs, nb_down_sample, *, share_model=None, **config):
        super().__init__(name, inputs, **config)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({
            'nb_down_sample': 3,
            'loss_weight': 1.0,
            'share_model': False
        }, super()._default_config())

    def _get_node(self, node_type, down_sample_ratio, source=None):
        if source is None:
            source = self.nodes
        name = "{}/image{}x".format(node_type, 2**down_sample_ratio)
        return source[name]

    def _kernel(self, feeds):
        x = None
        r = None
        losses = []
        for i_down_sample in reversed(range(1, self.param('nb_down_sample') + 1)):
            if x is None:
                x = self._get_node('input', i_down_sample, feeds)
            mid_result = SuperResolution2x('sr2x_{}'.format(i_down_sample),
                                           {NodeKeys.INPUT: x,
                                            NodeKeys.LABEL: self._get_node('label', i_down_sample - 1, feeds),
                                            SRKeys.REPRESENTS: r})()
            x = mid_result[NodeKeys.INFERENCE]
            if NodeKeys.LOSS in mid_result:
                losses.append(mid_result[NodeKeys.LOSS])
            r = mid_result[SRKeys.REPRESENTS]
        result = {NodeKeys.INFERENCE: x}
        if len(losses) > 0:
            with tf.name_scope('loss'):
                if not isinstance(self.param('loss_weight'), (list, tuple)):
                    lw = [self.param('loss_weight')] * \
                        self.param('nb_down_sample')
                else:
                    lw = self.param('loss_weight')
                for i, l in enumerate(losses):
                    losses[i] = losses[i] * lw[i]
                result[NodeKeys.LOSS] = tf.add_n(losses)
        return result
