import glob
import json
from dataclasses import asdict

from airflow import DAG
from airflow.operators.empty import EmptyOperator

from utils.dag_config import DagConfig


def auto_generate_dag(config: DagConfig) -> DAG:
    """Generate and return a dag"""

    doc_md = f"""
    # Auto generated dag

    Generated with this config: ```{asdict(config)}```
    """
    dag = DAG(
        dag_id=config.dag_id,
        description=f"Auto generated dag: {config.dag_id}",
        schedule=config.schedule,
        catchup=config.catchup,
        start_date=config.start_date,
        doc_md=doc_md,
        tags=["auto"],
    )

    return dag


def get_dag_configs() -> list[DagConfig]:
    """Read all dag config json files and return a list of `DagConfig`s"""
    dag_configs = []
    for file_path in glob.glob("dags/dag_configs/*.json"):
        with open(file_path, "r") as f:
            dag_config_json = json.load(f)
            dag_config = DagConfig(**dag_config_json)
            dag_configs.append(dag_config)

    return dag_configs


def add_tasks_to_dag(dag: DAG, dag_config: DagConfig) -> None:
    previous_task = None
    for task_id in dag_config.task_ids:
        task = EmptyOperator(task_id=task_id, dag=dag)

        if previous_task is not None:
            previous_task.set_downstream(task)

        previous_task = task


def generate_dags() -> None:
    """Auto generate dags"""
    dag_configs = get_dag_configs()

    for dag_config in dag_configs:
        dag = auto_generate_dag(dag_config)
        add_tasks_to_dag(dag, dag_config)
        globals()[dag.dag_id] = dag


if __name__ == "__main__":
    pass
else:
    generate_dags()
