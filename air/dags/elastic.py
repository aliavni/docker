#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""This dag tests performance of simple bash commands executed with Airflow."""

from __future__ import annotations

import datetime

from airflow.models.dag import DAG

from airflow.providers.standard.operators.bash import BashOperator

args = {
    "owner": "airflow",
    "start_date": datetime.datetime(2022, 1, 1),
}

dag = DAG(
    dag_id="perf_dag_1",
    default_args=args,
    schedule="@daily",
    dagrun_timeout=datetime.timedelta(minutes=60),
)

task_1 = BashOperator(
    task_id="perf_task_1",
    bash_command='sleep 5; echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag,
)

for i in range(2, 5):
    task = BashOperator(
        task_id=f"perf_task_{i}",
        bash_command="""
            sleep 5; echo "run_id={{ run_id }} | dag_run={{ dag_run }}"
        """,
        dag=dag,
    )
    task.set_upstream(task_1)

if __name__ == "__main__":
    dag.cli()
