from air.dags.utils.dag_config import DagConfig
from pendulum import DateTime, Timezone


class TestDagConfig:
    def test_parses_start_date(self):
        dc = DagConfig(dag_id="test-1", catchup=False, start="2024-01-01", task_ids=[])

        assert dc.start_date == DateTime(2024, 1, 1, tzinfo=Timezone("UTC"))
