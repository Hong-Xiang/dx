def create_global_scalars():
    from . import global_global_step
    from . import global_keep_prob
    import tensorflow as tf
    # global_global_step.create()
    tf.train.get_or_create_global_step()
    global_keep_prob.create()
