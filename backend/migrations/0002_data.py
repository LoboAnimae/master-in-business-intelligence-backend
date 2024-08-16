import os.path
from ..models import *
import pandas as pd
from django.db import migrations


def get_raw_data_path(name: str) -> pd.DataFrame:
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dirpath, 'raw_data', name)


def get_csv(name: str) -> pd.DataFrame:
    raw_data_path = get_raw_data_path(name)
    return pd.read_csv(raw_data_path, encoding='utf-8')


def get_excel(name: str):
    raw_data_path = get_raw_data_path(name)
    return pd.read_excel(raw_data_path, header=0)


def get_model(apps, name):
    return apps.get_model('backend', name)


def Application_populate(apps):
    data = get_csv('id_aplicacion.csv')
    model = apps.get_model('backend', 'Application')
    for _, row in data.iterrows():
        model.objects.create(
            id=row["ID"],
            name=row['Aplicación']
        )


def SimultaneousJobsDayWeek_populate(apps):
    data = get_excel('jobs_simultaneos_hora_dia_mes.xlsx')
    model = apps.get_model('backend', 'SimultaneousJobsDayWeek')
    for _, row in data.iterrows():
        hour = row['hora']
        day_of_month = row['Day of month']
        jobs_done = row['cant_jobs']
        model.objects.create(
            hour=hour,
            day_of_month_id=day_of_month,
            amount_jobs_done=jobs_done
        )


def HourDayWeekLatency_populate(apps):
    data: pd.DataFrame = get_excel('latencia_hora_dia_semana.xlsx')
    model = apps.get_model('backend', 'HourDayWeekLatency')
    for _, row in data.iterrows():
        model.objects.create(
            hour=row['hora'],
            day_of_week_id=row['ID Day of week'],
            latency=row['latencia_media']
        )


def HourDayMonthLatency_populate(apps):
    data: pd.DataFrame = get_excel('latencia_hora_dia_mes.xlsx')
    model = apps.get_model('backend', 'HourDayMonthLatency')
    for _, row in data.iterrows():
        model.objects.create(
            hour=row['hora'],
            day_of_month_id=row['Day of month'],
            latency=row['latencia_media'],
        )


def Scheme_populate(apps):
    data: pd.DataFrame = get_excel('tablas_disponibles.xlsx')
    model = apps.get_model('backend', 'Scheme')
    for name in data['esquema'].unique().tolist():
        model.objects.create(
            name=name
        )


def Table_populate(apps):
    data: pd.DataFrame = get_excel('tablas_disponibles.xlsx')
    model = apps.get_model('backend', 'Table')
    scheme_model = apps.get_model('backend', 'Scheme')
    for _, row in data.iterrows():
        scheme = scheme_model.objects.get(name=row['esquema'])
        name = row['tabla']
        model.objects.create(
            name=name,
            scheme=scheme
        )
        
def TableMetrics_populate(apps):
    data: pd.DataFrame = get_excel('metricas_por_tabla.xlsx')
    model = apps.get_model('backend', 'TableMetrics')
    scheme_model = apps.get_model('backend', 'Scheme')
    table_model = apps.get_model('backend', 'Table')
    for _, row in data.iterrows():
        scheme_instance = scheme_model.objects.get(name=row['esquema'])
        table_instance = table_model.objects.get(name=row['tabla'], scheme=scheme_instance)
        
        model.objects.create(
            scheme=scheme_instance,
            table=table_instance,
            mean_st=row['mean_st'],
            std_st=row['std_st'],
            min=row['min'],
            max=row['max'],
            initial_range=row['rango_inicial_by_table'],
            final_range=row['rango_final_by_table'],
            table_response_size=row['tamañano_resp_by_table'],
        )
        


def insert_data(apps, _):
    Application_populate(apps)
    SimultaneousJobsDayWeek_populate(apps)
    HourDayWeekLatency_populate(apps)
    HourDayMonthLatency_populate(apps)
    Scheme_populate(apps)
    Table_populate(apps)
    TableMetrics_populate(apps)


class Migration(migrations.Migration):
    atomic = True
    dependencies = [
        ('backend', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data),

    ]
