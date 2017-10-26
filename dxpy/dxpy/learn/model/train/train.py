from .base import Net


class Trainer(Net):
    def __init__(self, name, losses, variables):
        """
        Inputs:
            config: Configs;
            loss: Tensor;
        """
        super(__class__, self).__init__(config)
        self.loss = losses
        self.variables = variables
        self.learning_rate = self._get_learning_rate()
        self.optimizer = self._get_optimizer()
        self.nodes['train_step'] = self._get_train_step()

    def _get_optimizer(self):
        if self.config['optimizer']['name'].upper() == 'ADAM':
            return tf.train.

    def _get_learning_rate(self):
        self.add_node('learning_rate', shape=[], is_gpu=)
        initializer = tf.constant([23, 42])

    def _get_gradient(self):
        from ..utils.graph import device_name
        results = []
        if self.config.get('is_multi_gpu'):
            for i in range(self.config.get('nb_gpu')):
                with tf.device(device_name('gpu', i)):
                    results.append(self.optimizer.compute_gradients(
                        self.loss[i], self.train_vars))
        else:
            results.append(self.optimizer.compute_gradients(
                self.loss, self.train_vars))
        return results

    def _get_train_step(self, tower_grads, optimizer, summary_callback, name='train_step', clipv=None):
        """
        Inputs:
            tower_grads: *list or tuple* of grads
            optimizer: optimizer
        """
        with tf.name_scope(name), tf.device('/cpu:0'):
            average_grads = []
            for grad_and_vars in zip(*tower_grads):
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
                if clipv is not None:
                    grad = tf.clip_by_value(grad, -clipv, clipv)
                # Keep in mind that the Variables are redundant because they are shared
                # across towers. So .. we will just return the first tower's pointer to
                # the Variable.
                v = grad_and_vars[0][1]
                grad_and_var = (grad, v)
                average_grads.append(grad_and_var)
            train_op = optimizer.apply_gradients(
                average_grads, global_step=self.gs)

            if summary_callback is not None:
                summary_callback(average_grads)
        return train_op

    def run(self, session, task, feeds):
        pass


class TFTrainer(Trainer):
    pass
    # def _set_train(self):
    #     """ Construct train steps.
    #     After calling this method, all train_steps[train_tasks.kyes()] should be constructed.

    #     Automatically construct train/sub_task tasks with sub_task in train_tasks.
    #     Be careful on naming:
    #         train_tasks: list of sub_task names
    #         losses: dict of losses, value can be scalar(single gpu) or list of scalar(multi gpus)
    #         optimizers: dict of optimizers

    #     Generate:
    #         grads
    #         train_steps

    #     """
    #     # TODO: seperate optimizer getter.
    #     for k in self.train_tasks:
    #         with tf.name_scope('train_step_' + k):
    #             optim = self._get_optimizer(k)
    #             var_list = self._get_train_vars(k)
    #             if self.is_multi_gpu:
    #                 self.grads = defaultdict(list)
    #                 for i in range(self.p.nb_gpus):
    #                     with tf.device('/gpu:%d' % i):
    #                         self.grads[k].append(optim.compute_gradients(
    #                             self.losses[k][i], var_list))
    #                     # TODO: test perfomance of train step on cpu/gpus
    #                 with tf.device('/cpu:0'):
    #                     self.train_steps[k] = self.train_step(
    #                         self.grads[k], optim, self.p.summary_train)
    #             else:
    #                 self.grads[k] = optim.compute_gradients(
    #                     self.losses[k], var_list)
    #                 self.train_steps[k] = self.train_step(
    #                     [self.grads[k]], optim, self.p.summary_train)

    # def train_step(self, tower_grads, opt, is_summary=False, name='train_step'):
    #     from .ops import train_step
    #     from .ops import summary_var
    #     summary = summary_var if is_summary else None
    #     return train_step(tower_grads, opt, summary, name='train_step', self.params['grad_clip'])

    # def reset_lr(self, name=None, lr=None, decay=10.0):
    #     """ reset learning rate by value or decay.
    #     """
    #     if name is None:
    #         for n in self.params['lr'].keys():
    #             self.reset_lr(n, lr, decay)
    #         return None
    #     if lr is None:
    #         self.params['lr'][name] /= decay
    #     else:
    #         self.params['lr'][name] = lr
    #     pp_json(self.params, self.params['name'] + " PARAMS:")
