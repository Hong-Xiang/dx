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


def create_task_graph(tasks, depens):
    assert_same_length((tasks, depens), ('tasks', 'depens'))

    depens_tasks = []
    for i, ds in enumerate(depens):
        if ds is None:
            depens_tasks.append([None])
        elif isinstance(ds, int):
            depens_tasks.append([tasks[ds]])
        else:
            depens_tasks.append([tasks[d] for d in ds])
    return DenpensGraph(tasks, depens_tasks)


# def create_observable(task):
#     return rx.Observable.just(task)


# def try_create_task_db_record(task, g, creator):
#     def create_task(task, creator)
#         task.id = creator(task)
#         return task

#     def update_dependency(task):
#         task.dependency = [t.id for t in g.depends(task)]
#         return task

#     def all_depens_added(task):
#         return all([t in done for t in g.depens(task)])

#     return (task
#             .filter(all_depens_added)
#             .map(update_dependency).map(create_task))


# def update_done(task_ob, done_ob):
#     def add_elm(e, d):
#         if not e in d:
#             done.append(e)
#         return done
#     return task_ob.zip(done_ob, add_elm)


# def create_observable_graph(g, creator):
#     nb_elm = len(g)
#     done = []
#     source = g.nodes()
#     done_ob = rx.Observable.just(done).do_while(lambda t: len(done) < nb_elm)
#     sor_ob = rx.Observable.from_(source).repeat()
#     tasks_not_added = sor_ob.zip_array(done_ob).filter(
#         lambda x: not x[0] in x[1]).map(lambda x: x[0])
#     tasks_added = try_create_task_db_record(tasks_not_added, g, creator)
#     return update_done(tasks_added, done_ob)
