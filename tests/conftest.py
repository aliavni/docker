import pytest
from utils.dag_config import DagConfig


@pytest.fixture(scope="function")
def dag_config() -> DagConfig:
    dc = DagConfig(
        dag_id="test-dag-1",
        start="2024-07-24",
        task_ids=[],
        schedule=None,
        catchup=False,
    )
    return dc
