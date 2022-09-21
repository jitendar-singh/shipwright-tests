from behave import given, then, when, step
from kubernetes import client
from hamcrest import assert_that, equal_to
from resources import ResourcesModel

@then(u'the user creates a namespace for the registry')
def create_namespace(context):
    v1 = client.CoreV1Api()
    ns_body = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata={
            "name": "myregistry"
        }
    )
    namespace = v1.create_namespace(ns_body)
    assert_that(namespace.metadata.name, "myregistry")

@then(u'creates a deployment using the "registry:2" image')
def create_deployment(context):
    r = ResourcesModel()
    dep_body = r.get_deployment(object_name="myregistry")
    appsv1 = client.AppsV1Api()
    deployment = appsv1.create_namespaced_deployment(namespace="myregistry", body=dep_body)
    assert_that(deployment.metadata.name, "myregistry")

@then(u'create a service to expose the service ports on all nodes on the cluster')
def step_impl(context):
    pass