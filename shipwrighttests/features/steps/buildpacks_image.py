from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from resources import ResourcesModel

@then(u'the user generates a secret to access our container registry, such as one on Docker Hub or Quay.io:')
def generate_secret(context):
    """Create a new secret

    Args:
        context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes.

    Raises:
        ActivityFailed: When cannot process the API request
    """    
    v1 = client.CoreV1Api()
    secret_body = client.V1Secret(api_version="v1",
    kind="Secret",
    metadata=client.V1ObjectMeta(name="test-pull-secret",namespace="default"),
    type="kubernetes.io/dockerconfigjson",
    data={".dockerconfigjson": "ewogICJhdXRocyI6IHsKICAgICJxdWF5LmlvIjogewogICAgICAiYXV0aCI6ICJjM1Z1Ym5samIyNWphWE5sT21rM05EUklSbHB6TUVKcFMwUkNiVzF6VHpoVVVEbHhNSFpQVFZkTU1HcHhTM0ZKZFZkUmJsSlhTRmxNY2pSQ1JFVTJORXR5YTNSNGVHVnFNbHBTVTJNPSIsCiAgICAgICJlbWFpbCI6ICIiCiAgICB9CiAgfQp9"})
    try:
        v1.create_namespaced_secret('default', secret_body)
    except ApiException as e:
        raise ActivityFailed("Failed to create secret: {e}".format(e=str(e)))
    secret = v1.read_namespaced_secret('test-pull-secret', namespace='default')
    print('Secret: %s' %secret.metadata.name,' created')

@then(u'the user creates a custom build object')
def create_crd(context):
    """Create namespaced custom objects Build

    Args:
        context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes.
    """
    body = client.V1CustomResourceDefinition(api_version='shipwright.io/v1alpha1',
       kind='Build',
       metadata=client.V1ObjectMeta(name='buildpack-nodejs-build'),
       spec={"source":{
        "url":"https://github.com/shipwright-io/sample-nodejs",
        "contextDir": "source-build"},
        "strategy":{
            "name": "buildpacks-v3",
            "kind": "ClusterBuildStrategy"
        },
        "output":{
            "image": "registry.registry.svc.cluster.local:32222/samples/sample-nodejs:latest"
            # "credentials": {"name": "test-pull-secret"}
            }
       })
    custobjapi = client.CustomObjectsApi()
    try:
        custobjapi.create_namespaced_custom_object(group='shipwright.io', version='v1alpha1', namespace='default', plural='builds', body=body)
    except ApiException as ex:
        if ex.status != 404:
            raise

@then(u'the user creates a buildrun for the build')
def create_buildrun(context):
    """Create namespaced custom objects BuildRun

    Args:
        context (_type_): It holds the contextual information during the execution of tests.
		It is an object that can store user-defined data along with
		Python Behave-defined data, in context attributes.
    """
    buildrun_body = client.V1CustomResourceDefinition(api_version='shipwright.io/v1alpha1',
        kind='BuildRun',
        metadata=client.V1ObjectMeta(generate_name='buildpack-nodejs-buildrun-'),
        spec={"buildRef":{
            "name":"buildpack-nodejs-build"}
        }
    )
    custobjapi = client.CustomObjectsApi()
    try:
        custobjapi.create_namespaced_custom_object(group='shipwright.io', version='v1alpha1', namespace='default', plural='buildruns', body=buildrun_body)
    except ApiException as ex:
        if ex.status != 404:
            raise
