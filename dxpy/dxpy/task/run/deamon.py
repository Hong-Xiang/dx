
from .service import auto_complete, auto_submit, auto_start, update_complete


class DeamonService:
    @classmethod
    def cycle():
        from .service import auto_complete, auto_submit, auto_start
        auto_complete()
        auto_submit()
        auto_start()

    @classmethod
    def start(cls, cycle_intervel=None):
        from apscheduler.schedulers.blocking import BlockingScheduler
        scheduler = BlockingScheduler()
        scheduler.add_job(cycle_kernel, 'interval', seconds=10)
        print(
            'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

    @staticmethod
    def stop():
        raise NotImplementedError

    @staticmethod
    def restart():
        raise NotImplementedError

    @staticmethod
    def is_running():
        pass
