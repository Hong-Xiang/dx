from dxpy.learn.dataset.api import get_dataset
from dxpy.learn.net.api import get_network
from dxpy.learn.session import SessionDist
from tqdm import tqdm
from dxpy.learn.graph import NodeKeys
import time


def main(task='train', job_name='worker', task_index=0, cluster_config='cluster.yml'):
    from dxpy.learn.distribute.cluster import get_cluster_spec, get_server, get_nb_tasks
    from dxpy.learn.distribute.dataset import get_dist_dataset
    from dxpy.learn.distribute.ps import get_dist_network as get_ps_network
    from dxpy.learn.distribute.worker import apply_dist_network
    # from dxpy.learn.distribute.worker import get_dist_network as get_worker_network
    from dxpy.learn.utils.general import pre_work
    cluster = get_cluster_spec(cluster_config)
    server = get_server(cluster, job_name, task_index)
    dataset = get_dist_dataset(name='cluster/dataset/task0')
    if job_name == 'dataset':
        server.join()
        return
    if job_name in ['ps', 'worker', 'test', 'saver']:
        pre_work(device='/job:ps/task:0')
        network = get_ps_network(name='cluster/ps/task0', dataset=dataset)
        result_main = network()
    if job_name == 'ps':
        sess = SessionDist(target=server.target)
        with sess.as_default():
            network.post_session_created()
            sess.post_session_created()
            network.load()
        server.join()
        return
    if job_name == 'worker':
        # network_worker = get_worker_network(
        #     name='cluster/worker/task{}'.format(task_index), dataset=dataset)
        # result = network_worker()
        result = apply_dist_network(network=network, dataset=dataset, name='cluster/worker/task{}'.format(task_index))
        sess = SessionDist(target=server.target)
        with sess.as_default():
            for _ in tqdm(range(40)):
                for _ in range(100):
                    network.train()
                print(sess.run(result[NodeKeys.LOSS]))
        while True:
            time.sleep(1)
        return
    if job_name == 'test':
        sess = SessionDist(target=server.target)
        from dxpy.learn.scalar import global_step
        with sess.as_default():
            xv, yv, yp, loss, gs = sess.run([dataset['x'],
                                         dataset['y'],
                                         result_main[NodeKeys.INFERENCE],
                                         result_main[NodeKeys.LOSS], global_step()])
            print(xv)
            print(yv)
            print(yp)
            print(loss)
            print(gs)
        while True:
            time.sleep(1)
    if job_name == 'saver':

        network.save()