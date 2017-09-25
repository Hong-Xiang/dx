from .service import auto_complete, auto_submit, auto_start, update_complete

to_complete = []


def cycle_kernel():
    auto_complete()
    auto_submit()
    auto_start()


def launch_deamon(cycle_intervel=None):
    (Observable.interval(interval).start_with(0)
     .subscribe(on_next=lambda i: cycle_kernel(),
                on_error=lambda e: print(e, file=sys.stderr)))


class DeamonService:
    @staticmethod
    def start():
        launch_deamon()

    @staticmethod
    def stop():
        raise NotImplementedError

    @staticmethod
    def restart():
        raise NotImplementedError

    @staticmethod
    def is_running():
        pass
