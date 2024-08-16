
from django.db import models


class Application(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=152)

    def as_json(self):
        return {'id': self.id, 'name': self.name}


class SimultaneousJobsDayWeek(models.Model):
    hour = models.IntegerField()
    day_of_month_id = models.IntegerField()
    amount_jobs_done = models.IntegerField()


class HourDayWeekLatency(models.Model):
    hour = models.IntegerField()
    day_of_week_id = models.IntegerField()
    latency = models.FloatField()


class HourDayMonthLatency(models.Model):
    hour = models.IntegerField()
    day_of_month_id = models.IntegerField()
    latency = models.FloatField()


class Scheme(models.Model):
    name = models.CharField(max_length=1024)

    def as_json(self):
        return {'id': self.id, 'name': self.name}


class Table(models.Model):
    name = models.CharField(max_length=1024)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

    def as_json(self):
        return {'id': self.id, 'name': self.name, 'scheme': self.scheme.as_json()}


class TableMetrics(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    mean_st = models.FloatField()
    std_st = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    initial_range = models.FloatField()
    final_range = models.FloatField()
    table_response_size = models.FloatField()

    def as_json(self):
        return {
            'scheme': self.scheme.as_json(),
            'table': self.table.as_json(),
            'mean_st': self.mean_st,
            'std_st': self.std_st,
            'min': self.min,
            'max': self.max,
            'initial_range': self.initial_range,
            'final_range': self.final_range,
            'table_response_size': self.table_response_size,
        }
