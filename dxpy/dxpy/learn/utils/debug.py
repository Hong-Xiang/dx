import tensorflow as tf
from fs.osfs import OSFS


def dummy_image(shape=None, batch_size=32, nb_channel=1, name='dummy_image'):
    if shape is None:
        shape = [28, 28]
    return tf.placeholder(tf.float32, [batch_size] + shape + [nb_channel], name=name)


def write_graph(path=None):
    from .general import pre_work
    from ..train.summary import SummaryWriter
    from ..session import Session
    with OSFS('/tmp') as fs:
        dir_name = 'tf_tests'
        if fs.exists(dir_name):
            d = fs.opendir(dir_name)
        else:
            d = fs.makedir(dir_name)
        if d.exists('summary/train'):
            d.removetree('summary/train')
        summary = SummaryWriter(name='train',
                                path=d.getsyspath('summary/train'))
        session = Session()
        with session.as_default():
            summary.post_session_created()
