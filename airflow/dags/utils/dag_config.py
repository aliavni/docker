from dataclasses import dataclass
from typing import Union, List

import pendulum
from pendulum import DateTime


@dataclass
class DagConfig:
    dag_id: str
    schedule: Union[str, None]
    catchup: bool
    start: Union[str, None]
    task_ids: List[str]

    @property
    def start_date(self) -> DateTime:
        return pendulum.parse(self.start)
