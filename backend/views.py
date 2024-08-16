import json
import pickle
import joblib
import pandas as pd
from django.http import JsonResponse
from django.views import View
from .models import *
import os.path
from django.db.models import Avg


def as_day_event(hour: int):
    if hour <= 6:
        return "Madrugada"
    elif hour <= 11:
        return "Mañana"
    elif hour <= 14:
        return "Medio dia"
    elif hour <= 18:
        return "Tarde"
    return "Noche"


class ClassificationModel:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.preprocessor = joblib.load(os.path.join(
            dir_path, 'processor_models', 'preprocessor_class.pkl'))
        self.model = joblib.load(os.path.join(
            dir_path, 'processor_models', 'random_fores.pkl'))

    def predict(self, data):
        data = self.preprocessor.transform(data)
        return self.model.predict(data)

    def passes(self, data):
        result = self.predict(data)
        return result[0] == 'NORMAL'


class RegressionModel:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.preprocessor = joblib.load(os.path.join(
            dir_path, 'processor_models', 'preprocessor.pkl'))
        self.model = joblib.load(os.path.join(
            dir_path, 'processor_models', 'random_fores_reg.pkl'))

    def predict(self, data):
        data = self.preprocessor.transform(data)
        return self.model.predict(data)

    def get_prediction(self, data):
        result = self.predict(data)
        return result[0]


class PredictionView(View):
    def __init__(self):
        super().__init__()
        self.classification_model = ClassificationModel()
        self.regression_model = RegressionModel()

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        predictor_values = pd.DataFrame(columns=[
            'tabla',
            'app',
            'Day of month',
            'ID Day of week',
            'min',
            'max',
            'rango_inicial_by_table',
            'rango_final_by_table',
            'tamañano_resp_by_table',
            'Evento del Dia',
            'SimultJobs',
            'latencia_by_day_month',
            'latencia_by_day_week'
        ])

        predictor_values['tabla'] = [Table.objects.get(id=body['table']).name]
        predictor_values['app'] = body['application']
        predictor_values['Day of month'] = body['dayInMonth']
        predictor_values['ID Day of week'] = body['day']
        predictor_values['min'] = body['min']
        predictor_values['max'] = body['max']
        predictor_values['rango_inicial_by_table'] = body['initial_range']
        predictor_values['rango_final_by_table'] = body['final_range']
        predictor_values['tamañano_resp_by_table'] = body['table_response_size']
        predictor_values['Evento del Dia'] = as_day_event(body['hour'])

        try:
            predictor_values['SimultJobs'] = SimultaneousJobsDayWeek.objects.get(
                hour=body['hour'], day_of_month_id=body['dayInMonth']).amount_jobs_done
        except:
            predictor_values['SimultJobs'] = SimultaneousJobsDayWeek.objects.all().aggregate(
                Avg('amount_jobs_done'))['amount_jobs_done__avg']

        try:
            predictor_values['latencia_by_day_month'] = HourDayMonthLatency.objects.get(
                hour=body['hour'], day_of_month_id=body['dayInMonth']).latency
        except:
            predictor_values['latencia_by_day_month'] = HourDayMonthLatency.objects.all().aggregate(
                Avg('latency'))['latency__avg']

        try:
            predictor_values['latencia_by_day_week'] = HourDayWeekLatency.objects.get(
                hour=body['hour'], day_of_week_id=body['day']).latency
        except:
            predictor_values['latencia_by_day_week'] = HourDayWeekLatency.objects.all().aggregate(
                Avg('latency'))['latency__avg']

        if self.classification_model.passes(predictor_values):
            return JsonResponse({'optimized': True})

        table = Table.objects.get(id=body['table'])
        scheme = Scheme.objects.get(id=body['scheme'])

        metrics = TableMetrics.objects.get(table=table, scheme=scheme)

        predictor_values.insert(
            len(predictor_values.columns), "std_st", metrics.std_st)
        predictor_values.insert(
            len(predictor_values.columns), "mean_st", metrics.mean_st)
        prediction = self.regression_model.get_prediction(predictor_values)
        return JsonResponse({'optimized': False, 'prediction': prediction})


def get_schemes(request):
    return JsonResponse({'schemes': [x.as_json() for x in Scheme.objects.all()]})


def get_tables(request):
    return JsonResponse({'tables': [x.as_json() for x in Table.objects.all()]})


def get_applications(request):
    return JsonResponse({'applications': [x.as_json() for x in Application.objects.all()]})


def get_params(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    scheme_name = body['scheme']
    table_name = body['table']
    scheme = Scheme.objects.get(id=scheme_name)
    table = Table.objects.get(id=table_name)
    metric = TableMetrics.objects.get(scheme=scheme, table=table)
    return JsonResponse({'params': metric.as_json()})
