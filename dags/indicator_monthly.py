import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.operators.python import PythonOperator
from airflow.sensors.bash import BashSensor
from airflow.operators.dummy_operator import DummyOperator

from shared import normalize_csv, load_csv_to_postgres
import indicator_monthly_sqls as sqls

default_args = {"owner": "airflow"}
connection_id = 'dwh'
default_end_time = '2999-12-31 23:59:59'

with DAG(
    dag_id="indicator_monthly",
    start_date=datetime.datetime(2020, 1, 1),
    schedule_interval="0 0 1 * *",
    default_args=default_args,
    catchup=False,
) as dag:
    dm_start = DummyOperator(task_id='dm_start')

    create_dm_uncompleted_order_created_before_this_month_table = PostgresOperator(
        task_id="create_dm_uncompleted_order_created_before_this_month_table",
        postgres_conn_id=connection_id,
        sql=sqls.create_dm_uncompleted_order_created_before_this_month_table,
    )

    transform_dm_uncompleted_order_created_before_this_month_able = PostgresOperator(
        task_id="transform_dm_uncompleted_order_created_before_this_month_able",
        postgres_conn_id=connection_id,
        sql=sqls.transform_dm_uncompleted_order_created_before_this_month_able,
    )

    dm_start >> create_dm_uncompleted_order_created_before_this_month_table >> transform_dm_uncompleted_order_created_before_this_month_able

    create_dm_uncompleted_order_created_within_this_month_table = PostgresOperator(
        task_id="create_dm_uncompleted_order_created_within_this_month_table",
        postgres_conn_id=connection_id,
        sql=sqls.create_dm_uncompleted_order_created_within_this_month_table,
    )

    transform_dm_uncompleted_order_created_within_this_month_able = PostgresOperator(
        task_id="transform_dm_uncompleted_order_created_within_this_month_able",
        postgres_conn_id=connection_id,
        sql=sqls.transform_dm_uncompleted_order_created_within_this_month_able,
    )

    dm_start >> create_dm_uncompleted_order_created_within_this_month_table >> transform_dm_uncompleted_order_created_within_this_month_able

