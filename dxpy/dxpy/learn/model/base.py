import tensorflow as tf
from ..graph import Graph, NodeKeys


class Model(Graph):
    """
    Graphs which do not support sofiscated tasks, just acts as an function.
    Configs:
        reuse: bool
        tensorflow_variable_scope: str=None, *NOT IMPLEMENTED YET*.
        lazy_create: bool=False, if is True, will not create graph on __init__.
    """

    def __init__(self, name, inputs=None, **config):
        super().__init__(name, **config)
        self._created = False
        self._scope = self.c.get('scope')
        self._inputs = self._inputs_standardization(inputs)
        if not self.param('lazy_create'):
            self._construct()
        self.register_main_task(self.apply)

    def tensors_need_summary(self):
        return dict()

    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({
            'lazy_create': False,
            'register_inputs': True,
            'register_outputs': True,
        })
        return result

    @classmethod
    def _default_inputs(cls):
        return dict()

    def _pre_create_out_scope(self):
        pass

    def _pre_create_in_scope(self):
        pass

    def _post_create_in_scope(self):
        pass

    def _post_create_out_scope(self):
        pass

    def _kernel(self, feeds):
        raise NotImplementedError

    def apply(self, feeds=None):
        if not self._created:
            self._inputs = self._inputs_standardization(feeds)
            self._construct()
            return self._outputs
        else:
            with tf.variable_scope(self._variable_scope, reuse=True):
                return self._kernel(self._inputs_standardization(feeds))

    def _create_inputs(self):
        with tf.name_scope('inputs'):
            inputs = self._inputs_standardization()
            for n in inputs:
                if isinstance(inputs[n], tf.Tensor):
                    self.register_node(n, inputs[n])
                else:
                    inputs[n] = self.create_placeholder_node(
                        tf.float32, inputs[n]['shape'], n)
                    self._inputs[n] = inputs[n]

    def _register_inputs(self):
        if self.c.get('register_inputs'):
            for n in self._inputs:
                self.register_node(n, self._inputs[n])

    def _register_outputs(self):
        if self.c.get('register_outputs'):
            for n in self._outputs:
                self.register_node(n, self._outputs[n])

    def _create(self):
        with tf.variable_scope(self._variable_scope, reuse=False) as scope:
            self._scope = scope
            self._create_inputs()
            self._register_inputs()
            self._pre_create_in_scope()
            self._outputs = self._outputs_standardization(
                self._kernel(self._inputs))

            self._post_create_in_scope()
            self._register_outputs()
        self._created = True

    def _construct(self):
        self._pre_create_out_scope()
        self._create()
        self._post_create_out_scope()

    @property
    def _variable_scope(self):
        if self._scope is None:
            return self.name.name
        else:
            return self._scope

    @classmethod
    def _tensor_dict_standardization(cls, tensors=None):
        if tensors is None:
            return dict()
        if isinstance(tensors, tf.Tensor):
            return {NodeKeys.MAIN: tensors}
        result = dict()
        for n in tensors:
            if tensors[n] is not None:
                result[n] = tensors[n]
        return result

    def _inputs_standardization(self, inputs=None):
        result = self._default_inputs()
        if hasattr(self, '_inputs'):
            result.update(self._inputs)
        result.update(self._tensor_dict_standardization(inputs))
        return result

    def _outputs_standardization(self, outputs):
        result = dict()
        result.update(self._tensor_dict_standardization(outputs))
        return result


models = dict()


def register_model(key, model):
    if not isinstance(model, Model):
        raise TypeError("Only Model is supported, got {}.".format(type(model)))
    if key in models:
        raise ValueError("Key {} already exists.".format(key))
    models[key] = model


def load_model(key):
    return models.get(key)
