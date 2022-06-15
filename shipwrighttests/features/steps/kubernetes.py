from behave import given, then, when, step

@given(u'the Kubernetes cluster is available')
def probe_cluster_available(context):
	pass

@then(u'"{deployment}" is deployed and "{state}" on "{namespace}" namespace')
def probe_deployment_state(context, deployment, state, namespace):
	pass