def supervisor(config, load_fn, save_fn):
    sv_para = {'summary_op': None}
    sms = config.save.frequency
    load_step = config.save.load_step
    if sms is not None:
        sv_para['save_model_secs'] = sms
    if load_step is not None:
        sv_para['init_fn'] = load_fn
    sv_para['saver'] = save_fn
    supervisor = tf.train.Supervisor(**sv_para)

    tf_config = tf.ConfigProto(
        log_device_placement=config.log.is_show_device_placement)
    tf_config.gpu_options.allow_growth = True
    sess = supervisor.prepare_or_wait_for_session(config=tf_config)
    return {'supervisor': supervisor, 'session': sess}


# def _set_sesssv(self):
#         from .supervisor import supervisor
#         result = supervisor(self.params)