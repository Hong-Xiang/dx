from ..graph import Graph
from .step import GlobalStep


class Trainer(Net):
    def __init__(self, name, loss, variables):
        """
        Inputs:
            loss: scalar or list of scalar (multi gpu)
            variables: list of tensors
        """
        super(__class__, self).__init__(name)
        self.loss = loss
        self.variables = variables
        self.create_node(tf.float32, [], 'learning_rate')
        self.optimizer = self._get_optimizer()
        self.register_main_node(self._get_train_step())
        self.register_task('to_feed', self._get_feed_dict)

    def _get_optimizer(self):
        return tf.train.AdamOptimizer(self.nodes['learning_rate'])

    def _get_gradients(self):
        from ...tensorflow_extension.utils import device_name
        results = []
        if self.c['is_multi_gpu']:
            for i in range(self.c['nb_gpu']):
                with tf.device(device_name('gpu', i)):
                    results.append(self.optimizer.compute_gradients(
                        self.loss[i], self.variables))
        else:
            results.append(self.optimizer.compute_gradients(
                self.loss, self.variables))
        return results

    def _get_feed_dict(self):
        return {self.nodes['learning_rate'], self.c['learning_rate']}

    def _get_train_step(self):
        """
        Inputs:
            tower_grads: *list or tuple* of grads
            optimizer: optimizer
        """
        from .global_step import global_step_tensor
        tower_gradients = self._get_gradients()
        with tf.name_scope('train_step'), tf.device('/cpu:0'):
            average_grads = []
            for grad_and_vars in zip(*tower_gradients):
                # Note that each grad_and_vars looks like the following:
                #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
                grads = []
                for g, _ in grad_and_vars:

                    # Add 0 dimension to the gradients to represent the tower.
                    expanded_g = tf.expand_dims(g, 0)

                    # Append on a 'tower' dimension which we will average over
                    # below.
                    grads.append(expanded_g)
                # Average over the 'tower' dimension.
                grad = tf.concat(axis=0, values=grads)
                grad = tf.reduce_mean(grad, 0)
                if self.c['with_clip']:
                    grad = tf.clip_by_value(
                        grad, -self.c['clipv'], self.c['clipv'])
                # Keep in mind that the Variables are redundant because they are shared
                # across towers. So .. we will just return the first tower's pointer to
                # the Variable.
                grad_and_var = (grad, grad_and_vars[0][1])
                average_grads.append(grad_and_var)
            train_op = self.nodes['optimizer'].apply_gradients(
                average_grads, global_step=global_step_tensor())

            # if summary_callback is not None:
            #     summary_callback(average_grads)
        return train_op

    def _train(self, feeds):
        sess = tf.get_default_session()
        sess.run(self.nodes['train_op'],
                 feed_dict={self.nodes['learning_rate']: self.c['learning_rate']}.update(feeds))
