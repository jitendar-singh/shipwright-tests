from kubernetes import client
class ResourcesModel(object):
    def __init__(self,crd_scope={},object_name=""):
        self.crd_scope = crd_scope

    def get_crd_scope(self, resource_name):
        """This method acts an model method used
           to get the scope of CustomResourceDefinitions
        Args:
            resource_name (str): Name of the CustomResourceDefinitions

        Returns:
            str: returns scope of the CustomResourceDefinitions i.e. Namespaced or Cluster
        """        
        scope = self.crd_scope[resource_name+'.shipwright.io']
        return scope
    
    def get_custom_objects(self, object_name):
        """This method acts an model method used
        to search the custom objects created by CustomResourceDefinitions

        Args:
            object_name (str): name of the custom object

        Returns:
            str: custom object
        """
        self.object_name = object_name
        cstobj = client.CustomObjectsApi()
        res = cstobj.get_cluster_custom_object('shipwright.io', 'v1alpha1', 'clusterbuildstrategies', self.object_name)
        return res["metadata"]["name"]
    
    def get_deployment(self,object_name):
        self.object_name = object_name
        NAMESPACE = self.object_name
        # configurate the pod template container
        container = client.V1Container(
            name="myregistry",
            image="registry:2",
            image_pull_policy="IfNotPresent",
            env=[client.V1EnvVar(name="REGISTRY_STORAGE_DELETE_ENABLED",value="true")],
            ports=[client.V1ContainerPort(container_port=5000,host_port=32222)],
            resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "128M"},
            limits={"cpu": "100m", "memory": "128M"}
            ),
        )

        # create and configure a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
            labels={"app":"myregistry"},
            namespace=NAMESPACE),
            spec=client.V1PodSpec(containers=[container]),
        )

        #Create the specification of deployment
        spec = client.V1DeploymentSpec(
            replicas=2,
            template=template,
            selector={
                "matchLabels":{"app":"myregistry"}
            }
        )

        # Instantiate the deployment object

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name="myregistry"),
            spec=spec,
        )

        return deployment