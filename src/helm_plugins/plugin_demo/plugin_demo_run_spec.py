from helm.benchmark.run_specs import run_spec_function
from helm.benchmark.adaptation.adapters.adapter_factory import ADAPT_GENERATION

from helm.benchmark.adaptation.adapter_spec import AdapterSpec
from helm.benchmark.runner import RunSpec
from helm.benchmark.scenarios.scenario import ScenarioSpec
from helm.benchmark.run_specs import get_basic_metric_specs
from helm.benchmark.metrics.metric import MetricSpec


@run_spec_function("plugin_demo")
def get_plugin_demo_spec() -> RunSpec:
    """A run spec for debugging."""
    scenario_spec = ScenarioSpec(
        class_name="helm_plugins.plugin_demo.plugin_demo_scenario.PluginDemoScenario",
        args={"num_input_tokens": 5, "vocab_size": 20, "num_train_instances": 10, "num_test_instances": 10},
    )
    adapter_spec = AdapterSpec(
        method=ADAPT_GENERATION,
        instructions="Please solve the following problem.\n",
        max_train_instances=5,
        max_eval_instances=10,
        num_outputs=3,
        num_train_trials=3,
        temperature=1,
        stop_sequences=["."],
    )
    return RunSpec(
        name="plugin_demo",
        scenario_spec=scenario_spec,
        adapter_spec=adapter_spec,
        metric_specs=get_basic_metric_specs([])
        + [MetricSpec(class_name="helm_plugins.plugin_demo.plugin_demo_metrics.PluginDemoMetric", args={})],
        groups=[],
    )
