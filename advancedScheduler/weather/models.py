import pytz
from django.db import models
import uuid
from datetime import timedelta, datetime
from django.db.models.signals import post_save, pre_save
from .utils.model_sts import Status
from .utils.updater import JobController
EXPIRE_PICKUP_TIME = 1


class Forecast(models.Model):
    timestamp = models.DateTimeField()
    temperatue = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.now()
        return super(Forecast, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}"


class Product(models.Model):
    name = models.CharField(max_length=120)
    state = models.IntegerField(default=0)
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return f"{self.name}"


class TriggerType(models.IntegerChoices):
    SHOW_ORDER_TO_OFFER = 1
    NOTIFY_DRIVER_EXP_ACCEPT = 2
    RETURN_TO_OFFER = 3


class JobStatus(models.IntegerChoices):
    CREATED = 1
    PROGRESS = 2
    DONE = 3
    FAILED = 4


class RunTrigger(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    time_run = models.DateTimeField(auto_now_add=False)
    status = models.IntegerField(choices=JobStatus.choices, default=JobStatus.CREATED)
    error = models.TextField(blank=True)

    def __str__(self):
        return f"Trigger-ID: {self.id}"

    class Meta:
        verbose_name = "TBRunTrigger"
        verbose_name_plural = "TBRunTriggers"
        ordering = ['-id']

    def logger(self, status, e: str = ""):
        print("LOGGER QS", status, type(status))
        try:
            self.time_run = datetime.now(tz=pytz.UTC)
            self.status = status
            self.error = e
            self.save()
            return True
        except Exception as e:
            print("Exception __logger", e.args)
            return False


class JobTrigger(models.Model):
    trigger = models.ForeignKey(
        RunTrigger, on_delete=models.CASCADE, null=True, blank=True, related_name='run_trigger')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.IntegerField(choices=TriggerType.choices)
    finished_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job-ID: {self.id}"

    class Meta:
        verbose_name = "TBJobTrigger"
        verbose_name_plural = "TBJobTriggers"
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.id:
            trigger = RunTrigger.objects.create(time_run=self.finished_time, status=JobStatus.CREATED)
            self.trigger = trigger
        return super(JobTrigger, self).save(*args, **kwargs)


class Order(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    expiry_pick_up_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return f"{self.get_status_display()}"

    def completed(self, order, run: RunTrigger):
        print("@1......", run)
        obj = run.logger(status=JobStatus.DONE)
        if self.id == order.id:
            self.status = Status.PICKUP
            self.save(update_fields=("status", ))
        return print(f"Job: \n{obj} {order, type(order)}")


def get_trigger_time():
    current_time = datetime.now(tz=pytz.UTC)
    if current_time.minute < 59:
        trigger_time = datetime.now(tz=pytz.UTC) + timedelta(minutes=2)
    else:
        trigger_time = datetime(
            current_time.year, current_time.month, current_time.day + 1, 16, 00, 00).replace(tzinfo=pytz.UTC)
    return trigger_time


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.timestamp = datetime.now(tz=pytz.UTC)
        instance.save()
    if instance.status == Status.ACCEPT and instance.expiry_pick_up_time is None:
        instance.expiry_pick_up_time = get_trigger_time()
        instance.save()
        job = JobTrigger.objects.create(
            type=TriggerType.RETURN_TO_OFFER,
            finished_time=instance.expiry_pick_up_time
        )
        JobController.start(order=instance, trigger=job.trigger)
post_save.connect(post_save_order, sender=Order)


def post_save_run_job(sender, instance, created, *args, **kwargs):
    if not created and instance.status == JobStatus.DONE:
        JobController.force_done(trigger=instance)
post_save.connect(post_save_run_job, sender=RunTrigger)
