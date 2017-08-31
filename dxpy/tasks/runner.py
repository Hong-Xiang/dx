import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def tasks_loop():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=tasks_loop,
        trigger=IntervalTrigger(seconds=5),
        id='task_runner',
        name='Check and run tasks every 10 seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    scheduler.start()


if __name__ == "__main__":
    main()
