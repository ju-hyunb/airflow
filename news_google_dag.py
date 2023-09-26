from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import os


dag = DAG(
    'news_google_dag',
    schedule_interval='* */1 * * *', #hourly 
    start_date=datetime.today(),
    catchup=False
)



run_script = BashOperator(
    task_id='run_news_google_script',
    bash_command='python ${AIRFLOW_HOME}/dags/NewsGoogle.py',
    dag=dag
)


def insert_data_to_db():
    
    from NewsGoogle import result_df
    from Driver import db_connection, dump

    engine, conn = db_connection()
    dump('newsgoogle', result_df, engine) 

    conn.close()


insert_data_task = PythonOperator(
    task_id='insert_data_to_db',
    python_callable=insert_data_to_db,
    dag=dag
)


# Set the task dependencies
run_script >> insert_data_task
