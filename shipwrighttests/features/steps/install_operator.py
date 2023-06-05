from behave import given, then, when, step
from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.config import ConfigException
from resources import ResourcesModel
from hamcrest import assert_that, equal_to

@when(u'the following "CustomResourceDefinition" are created')
def create_crds(context):
    #Process rows values from the table
    for row in context.table:
        kind = row['kind']
        object_name = row['name']
        api_version = row['api_version']

    rm = ResourcesModel()
    rm.create_custom_resource_definition(api_version, kind, object_name)

@then(u'we check the status of "CustomResourceDefinition"')
def assert_crds(context):
    pass 

@then(u'we check for the operator pod status in "openshift-marketplace" project')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we check for the operator pod status in "openshift-marketplace" project')