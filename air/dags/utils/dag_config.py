"""Dag configuration for Airflow DAGs."""

from dataclasses import dataclass
from typing import List, Optional, Union

import pendulum
from pendulum import DateTime


@dataclass
class DagConfig:
    """DagConfig is a configuration class for defining DAG parameters."""

    dag_id: str
    start: Union[str, None]
    task_ids: List[str]
    schedule: Optional[str] = None
    catchup: bool = False

    @property
    def start_date(self) -> DateTime:
        """Returns the start date as a pendulum DateTime object."""
        return pendulum.parse(self.start)
