class TaskRunService:
    """ run commands of tasks
    """
    @classmethod
    def check_complete(cls):
        from dxpy.task.task import TaskSbatch
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Runing)
            .filter(lambda t: isinstance(t, TaskSbatch))
            .subscribe(lambda t: t.check_complete())
        )

    @classmethod
    def submit(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.state.run == t.state.RunState.Pending)
            .filter(lambda t: not t.is_to_run)
            .flat_map(lambda t: t.dependence())
            .filter(lambda t: t.state.is_waiting_to_submit)
            .subscribe(lambda t: t.submit())
        )

    @classmethod
    def run(cls):
        (
            TaskStoreService.all()
            .filter(lambda t: t.is_to_run)
            .subscribe(lambda t: t.run())
        )

    @classmethod
    def cycle(cls):
        TaskRunService.check_complete()
        TaskRunService.submit()
        TaskRunService.run()

    @classmethod
    def launch_deamon(cls, interval=10000):
        Observable.interval(interval).start_with(0).subscribe(
            on_next=lambda t: TaskRunService.cycle(), on_error=lambda e: print(e))

    @classmethod
    def mark_as_finish(self, id_or_task):
        if isinstance(id_or_task, int):
            task = self.get(id_or_task)
        else:
            task = id_or_task
        task.finish()