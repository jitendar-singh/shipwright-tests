from behave import given, then, when, step

@given(u'the Kubernetes cluster is available')
def probe_cluster_available(context):
	pass

@then(u'"{deployment}" is deployed and "{state}" on "{namespace}" namespace')
def probe_deployment_state(context, deployment, state, namespace):
	pass

@then(u'the following resource names belong to "{api_version}" API version')
def probe_resources_for_apiversion(context, api_version):
	pass

@then(u'the following "{name}" objects are present')
def probe_cluster_objects(context, name):
	pass