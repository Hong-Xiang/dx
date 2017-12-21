from dxpy.configs import configurable
from dxpy.learn.config import config
from dxpy.learn.train.summary_2 import SummaryWriter
from .main import NodeKeys, SRKeys, SRNetKeys
import tensorflow as tf


class SRSummaryWriter(SummaryWriter):
    @configurable(config, with_name=True)
    def __init__(self, network, name='summary', **kw):
        summary_tensors = {
            'input_lr': network['inputs/input/image{}x'.format(2**network.param('nb_down_sample'))],
            'label': network['outputs/aligned_label'],
            'interp': network['outputs/interp'],
            'loss': network[NodeKeys.LOSS],
            'infer': network['outputs/inference'],
            'learning_rate': network['trainer']['learning_rate']['value']
        }
        nb_runs = {
            'loss': 32,
            'mes_inf': 32,
            'mse_itp': 32,
            'mse_inf_to_itp_ratio': 32,
        }
        super().__init__(name=name, tensors=summary_tensors, nb_runs=nb_runs, **kw)

    def _processing(self, tensors):
        from dxpy.learn.model.metrics import mse
        with tf.name_scope("processing"):
            result = {k: tensors[k] for k in tensors}
            res_inf = tf.abs(result['label'] - result['infer'])
            res_itp = tf.abs(result['label'] - result['interp'])
            dif_inf_itp = tf.abs(result['infer'] - result['interp'])
            result['res_inf'] = res_inf
            result['res_itp'] = res_itp
            result['dif_inf_itp'] = dif_inf_itp
            result['mse_inf'] = mse(result['label'], result['infer'])
            result['mse_itp'] = mse(result['label'], result['interp'])
            result['mse_inf_to_itp_ratio'] = result['mse_inf'] / \
                result['mse_itp']
        return super()._processing(result)


class SRSummaryWriter_v2(SummaryWriter):
    @configurable(config, with_name=True)
    def __init__(self, network, tensors, name='summary', **kw):
        summary_tensors = {
            'input_lr': tensors['input/image{}x'.format(2**network.param('nb_down_sample'))],
            'label': tensors['aligned_label'],
            'interp': tensors['interp'],
            'loss': tensors[NodeKeys.LOSS],
            'infer': tensors['inference'],
            'learning_rate': network['trainer']['learning_rate']['value']
        }
        if 'loss/l1' in tensors:
            summary_tensors.update({'loss_l1': tensors['loss/l1']})
        if 'loss/mse' in tensors:
            summary_tensors.update({'loss_mse': tensors['loss/mse']})
        if 'loss/poi' in tensors:
            summary_tensors.update({'loss_poi': tensors['loss/poi']})
        nb_runs = {
            'loss': 32,
            'mes_inf': 32,
            'mse_itp': 32,
            'mse_inf_to_itp_ratio': 32,
        }
        super().__init__(name=name, tensors=summary_tensors, nb_runs=nb_runs, **kw)

    def _processing(self, tensors):
        from dxpy.learn.model.metrics import mse
        with tf.name_scope("processing"):
            result = {k: tensors[k] for k in tensors}
            res_inf = tf.abs(result['label'] - result['infer'])
            res_itp = tf.abs(result['label'] - result['interp'])
            dif_inf_itp = tf.abs(result['infer'] - result['interp'])
            result['res_inf'] = res_inf
            result['res_itp'] = res_itp
            result['dif_inf_itp'] = dif_inf_itp
            result['mse_inf'] = mse(result['label'], result['infer'])
            result['mse_itp'] = mse(result['label'], result['interp'])
            result['mse_inf_to_itp_ratio'] = result['mse_inf'] / \
                result['mse_itp']
        from dxpy.debug.utils import dbgmsg
        dbgmsg(result)
        return super()._processing(result)
