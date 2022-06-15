
from behave import given, then, when, step

@given(u'the Kubernetes cluster is available')
def probe_cluster_available(context):
	pass

@then(u'"{deployment}" is deployed and "{state}" on "{namespace}" namespace')
def probe_deployment_state(context, deployment, state, namespace):
	pass

@then(u'we check namespace/shipwright-build should be created')
def step_impl(context):
   pass


@then(u'we check that the following resources are created')
def step_impl(context):
    pass


@then(u'check the following clusterbuildstrategy.shipwright.io/ are installed')
def step_impl(context):
    pass