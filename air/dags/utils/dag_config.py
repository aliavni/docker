from dataclasses import dataclass
from typing import Union, List, Optional

import pendulum
from pendulum import DateTime


@dataclass
class DagConfig:
    dag_id: str
    start: Union[str, None]
    task_ids: List[str]
    schedule: Optional[str] = None
    catchup: bool = False

    @property
    def start_date(self) -> DateTime:
        return pendulum.parse(self.start)
