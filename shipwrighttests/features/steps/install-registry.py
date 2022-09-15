from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.config import ConfigException

DEPLOYMENT_NAME = "registry"

def connect_cluster():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
            print("Connection to the cluster initiated")
            print("Active host is %s" % configuration.Configuration().host)
        except config.ConfigException:
            raise Exception("cluster probe failed")
        print("***Connected to cluster***")

def create_namespace():
    v1 = client.CoreV1Api()
    ns_body = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata={
            "name": "registry"
        }
    )
    res = v1.create_namespace(ns_body)
    return res.metadata.name

def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="registry",
        image="registry:2",
        image_pull_policy="IfNotPresent",
        env=[client.V1EnvVar(name="REGISTRY_STORAGE_DELETE_ENABLED",value="true")],
        ports=[client.V1ContainerPort(container_port=5000,host_port=32222)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "128M"},
            limits={"cpu": "100m", "memory": "128M"},
        ),
    )

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "registry"},namespace="registry"),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1, template=template, selector={
            "matchLabels":
            {"app": "registry"}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec,
    )

    return deployment

def create_service():
    v1 = client.CoreV1Api()
    service_body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata={
            "labels":
            {"app": "registry"},
            "name": "registry",
            "namespace": "registry"
        },
        spec= client.V1ServiceSpec(
            ports=[client.V1ServicePort(port=32222,node_port=32222,protocol="TCP",target_port=5000)],
            selector={"app": "registry"},
            type="NodePort"
        )
    )
    service = v1.create_namespaced_service('registry', service_body)
    return service.metadata.name


connect_cluster()
registry_namespace = create_namespace()
print('INFO: Namespace: ',registry_namespace,' created')
deployment_body = create_deployment_object()
appsv1 = client.AppsV1Api()
deploy = appsv1.create_namespaced_deployment(namespace='registry',body= deployment_body)
print("INFO: Deployment: ",deploy.metadata.name," created")
svc = create_service()
print("INFO: Service: ",svc," created")
