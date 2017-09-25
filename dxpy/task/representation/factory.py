import rx
from collections import namedtuple
from dxpy.graph.depens import DenpensGraph
from dxpy.exceptions.checks import assert_same_length
from .templates import template_class


def create_by_cls(template_class, *args, **kwargs):
    return template_class(*args, **kwargs)


def create_by_name(template_name, *args, **kwargs):
    return create_by_cls(template_class(template_name), *args, **kwargs)


def create(template_class_or_name, *args, **kwargs):
    if isinstance(template_class_or_name, str):
        return create_by_name(template_class_or_name, *args, **kwargs)
    else:
        return create_by_cls(template_class_or_name, *args, **kwargs)


def create_task_graph(template_list, args_list, kwargs_list, depends):
    assert_same_length((template_list, args_list, kwargs_list,
                        depends), 'template_names', 'args_list', 'kwargs_list', 'depens')
    tasks = [t create(tcls, a, kw) for tcls, a, kw in zip(template_list, args_list, kwargs_list)]
    return DenpensGraph(tasks, depends)


def create_observable(task):
    return rx.Observable.just(task)


def create_observable_graph(g, creator):
    done = []
    done_ob = rx.Observable.just(done).repeate()

    def add_done(t, d):
        d.append(t)

    nodes = rx.Observable.from_(g.nodes()).repeat(len(g.nodes()))
