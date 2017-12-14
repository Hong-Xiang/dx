from dxpy.learn.dataset.api import get_dataset
from dxpy.learn.net.api import get_network
from dxpy.learn.session import SessionDist
from tqdm import tqdm
from dxpy.learn.graph import NodeKeys
import time
import arrow
from dxpy.learn.scalar import global_step
import tensorflow as tf


def main(task='train', job_name='worker', task_index=0, cluster_config='cluster.yml'):
    from dxpy.learn.distribute.cluster import get_cluster_spec, get_server, get_nb_tasks
    from dxpy.learn.distribute.dataset import get_dist_dataset
    from dxpy.learn.distribute.ps import get_dist_network as get_ps_network
    from dxpy.learn.distribute.worker import apply_dist_network
    from dxpy.learn.distribute.summary import get_dist_summary
    from dxpy.learn.distribute.worker import get_dist_network as get_worker_network
    from dxpy.learn.utils.general import pre_work
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    cluster = get_cluster_spec(cluster_config, job_name=None)
    server = get_server(cluster, job_name, task_index, config=config)
    datasets = []
    nb_datasets = get_nb_tasks(cluster_config, 'dataset')
    for i in range(nb_datasets):
        datasets.append(get_dist_dataset(name='cluster/dataset/task{}'.format(i)))
    if job_name == 'dataset':
        server.join()
        return
    elif job_name == 'ps':
        server.join()
        return
    elif job_name in ['worker', 'summary']:
        with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:{}".format(task_index), cluster=cluster)):
            pre_work()
            network = get_network(name='network/srms', dataset=datasets[task_index % nb_datasets])
            result = network()
        if job_name == 'worker':
            hooks = [tf.train.StepCounterHook()]
            with tf.train.MonitoredTrainingSession(master=server.target,
                                                   is_chief=(task_index == 0),
                                                #    is_chief=True,
                                                   checkpoint_dir="./save",
                                                   config=config,
                                                   hooks=hooks) as sess:
                from dxpy.learn.session import set_default_session
                set_default_session(sess)
            # sess = SessionDist(target=server.target)
                # with sess._sess.as_default():
                for _ in tqdm(range(10000000000000), ascii=True):
                    network.train()
    if job_name == 'summary':
        name = 'cluster/summary/task{}'.format(task_index)
        result = apply_dist_network(
            network=network, dataset=datasets[-1], name=name)
        result.update(dataset[-1].nodes)
        sw = get_dist_summary(tensors=result, network=network, name=name)
        sess = SessionDist(target=server.target)
        with sess.as_default():
            sw.post_session_created()
            while True:
                sw.auto_summary()
        return
