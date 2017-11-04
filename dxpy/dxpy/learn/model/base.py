import tensorflow as tf
from ..graph import Graph, KEY_MAIN


class Model(Graph):
    """
    Graphs which do not support sofiscated tasks, just acts as an function.
    Configs:
        reuse: bool
        tensorflow_variable_scope: str=None, *NOT IMPLEMENTED YET*.
        lazy_create: bool=False, if is True, will not create graph on __init__.
    """

    def __init__(self, name, inputs=None, **config):
        super(__class__, self).__init__(name, **config)
        self.inputs = self.__inputs_standardization(inputs)
        self._created = False
        if not self.c.get('lazy_create', False):
            self.__create()
        self.register_main_task(self.apply)

    @classmethod
    def _default_inputs(self):
        return dict()

    @property
    def _variable_scope(self):
        return self.name.name

    def _kernel(self, feeds):
        raise NotImplementedError

    def apply(self, feeds=None):
        reuse = feeds.get('reuse', self._created)
        with tf.variable_scope(self._variable_scope, reuse=reuse):
            return self._kernel(self.__inputs_standardization(feeds))

    @classmethod
    def __tensor_dict_standardization(cls, tensors=None):
        if tensors is None:
            return dict()
        if isinstance(tensors, tf.Tensor):
            return {KEY_MAIN: tensors}
        return tensors

    def __inputs_standardization(self, inputs=None):
        result = self._default_inputs()
        if hasattr(self, 'inputs'):
            result.update(self.inputs)
        result.update(self.__tensor_dict_standardization(inputs))
        return result

    def __outputs_standardization(self, outputs):
        result = dict()
        result.update(self.__tensor_dict_standardization(outputs))
        return result

    def __create(self, feeds=None):
        with tf.variable_scope(self._variable_scope, reuse=False):
            with tf.name_scope('inputs'):
                inputs = self.__inputs_standardization(feeds)
                for n in inputs:
                    if isinstance(inputs[n], tf.Tensor):
                        self.register_node(n, inputs[n])
                    else:
                        inputs[n] = self.create_placeholder_node(
                            tf.float32, inputs[n]['shape'], n)
                        self.inputs[n] = inputs[n]
            outputs = self.__outputs_standardization(
                self._kernel(inputs))
            if self.c.get('register_outputs'):
                for n in outputs:
                    self.register_node(n, outputs[n])
        self._created = True
