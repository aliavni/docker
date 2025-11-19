from air.dags.generator import auto_generate_dag, get_dag_configs


class TestGenerator:
    def test_auto_generate_dag(self, dag_config):
        dag = auto_generate_dag(dag_config)

        assert dag.dag_id == dag_config.dag_id
        assert dag.start_date == dag_config.start_date
        assert dag.catchup == dag_config.catchup
        assert dag.schedule == dag_config.schedule

    def test_get_dag_configs(self):
        res = get_dag_configs()
        assert res == []
