import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta, datetime
# The "apscheduler." prefix is hard coded
scheduler = BackgroundScheduler()
scheduler.start()


class JobController:

    @classmethod
    def start(cls, order, trigger):
        print("Start.....", trigger, type(trigger))
        print("UNIQUE.....", trigger.unique_id, type(trigger.unique_id))
        scheduler.add_job(
            order.completed, 'date',
            run_date=trigger.time_run,
            id=str(trigger.unique_id),
            args=[order, trigger]
        )

    @classmethod
    def run(cls, order, trigger):
        scheduler.add_job(
            order.record_log, 'date',
            run_date=trigger.time_run,
            id=str(trigger.unique_id),
            args=[order, trigger]
        )

    @classmethod
    def remove_job(cls, trigger):
        print("reschedule.....", trigger, type(trigger))
        print("UNIQUE.....", trigger.unique_id, type(trigger.unique_id))
        job = scheduler.get_job(str(trigger.unique_id))
        print("JOB.....", job, type(job))
        if job:
            res = job.remove()
            print("Res......", res, type(res))
        else:
            print("job......", job, type(job))
        scheduler.print_jobs()

    @classmethod
    def force_done(cls, trigger):
        print(f"force_done.....{trigger, type(trigger)}")
        job = scheduler.get_job(str(trigger.unique_id))
        print("JOB.....", job, type(job))
        if job:
            now = datetime.now(tz=pytz.UTC)
            res = job.modify(next_run_time=now)
        else:
            print("job......", job, type(job))
        scheduler.print_jobs()


# def say_hello():
#     print("Block user....")
#
# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(say_hello, 'interval', minutes=1)

