from behave import given, then, when, step
from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.config import ConfigException
from resources import ResourcesModel
from hamcrest import assert_that, equal_to

@given(u'the Kubernetes cluster is available')
def probe_cluster_available(context):
	"""Probe if the cluster is available

	Args:
		context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes.

	Raises:
		config.ConfigException: When unable to load kubeconfig
	"""
	v1 = client.CoreV1Api()
	node_state = {}
	node_lst = v1.list_node()
	for nodes in node_lst.items:
		print("Evaluating node: ",nodes.metadata.name)
		node_status = v1.read_node_status(nodes.metadata.name)
		for status in node_status.status.conditions:
			node_state[status.type] = status.status
	if 'Ready' in node_state.keys():
		if node_state['Ready'] == 'True':
			print("INFO: Node ",nodes.metadata.name," status is: ",node_state['Ready'])
		else:
			raise Exception("ERR: Node ",nodes.metadata.name," status:",node_state['Ready'])

@then(u'"{deployment}" is deployed and "{state}" on "{namespace}" namespace')
def probe_deployment_state(context, deployment, state, namespace):
	"""Probe the state of deployments

	Args:
		context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes
		deployment (str): name of the deployment
		state (str): current state of the deployment
		namespace (str): namespace in which the deployment is present

	Raises:
		Exception: Raises a exception when deployment is not ready

	Returns:
			bool: True based on deployment state
	"""
	appsv1 = client.AppsV1Api()
	deployment_state = appsv1.read_namespaced_deployment_status(deployment, namespace)
	desired_replicas = deployment_state.spec.replicas
	ready_replicas = deployment_state.status.ready_replicas
	if desired_replicas == ready_replicas:
		print("INFO: Deployment ",deployment," desired replicas:<",desired_replicas,"> ready replicas:<",ready_replicas,">")
	else:
		raise Exception("ERR: Deployment ",deployment," desired replicas:<",desired_replicas,"> ready replicas:<",ready_replicas,">")
		
@then(u'the following resource names belong to "{api_version}" API version')
def probe_resources_for_apiversion(context, api_version):
	"""Probe the scope of CustomResourceDefinitions
		i.e. Namespaced or Cluster

	Args:
		context (_type_): It holds the contextual information during the execution of tests.
			It is an object that can store user-defined data along with
			Python Behave-defined data, in context attributes
		api_version (_type_): api version of the CustomResourceDefinitions
	"""
	crd_scope = {}
	cusobj = client.ApiextensionsV1Api()
	res = cusobj.list_custom_resource_definition()
	for item in res.items:
		crds = item.metadata.name
		scope = item.spec.scope
		crd_scope[crds]=scope

	model = getattr(context, "model", None)
	if not model:
		context.model = ResourcesModel(crd_scope)
	for row in context.table:
		res = context.model.get_crd_scope(row["resource_name"])
		assert_that(row["scope"],equal_to(res))

@then(u'the following "{name}" objects are present')
def probe_cluster_objects(context, name):
	"""Probe the availability of custom objects created by CustomResourceDefinitions

	Args:
		context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes
		name (str): name of the custom object
	"""
	cstobj = client.CustomObjectsApi()
	model = getattr(context, "model", None)
	if not model:
		context.model = ResourcesModel(crd_scope={},object_name="")
	for row in context.table:
		object_name = cstobj.get_cluster_custom_object('shipwright.io', 'v1alpha1', 'clusterbuildstrategies', row["name"])
		res = context.model.get_custom_objects(object_name["metadata"]["name"])
		assert_that(row["name"],equal_to(res))