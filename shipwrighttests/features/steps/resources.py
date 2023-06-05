from kubernetes import client
from kubernetes.client.exceptions import ApiException
class ResourcesModel(object):
    def __init__(self,crd_scope = {},object_name = "",kind = ""):
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

    def create_custom_resource_definition(self,api_version, kind, object_name):
        """This method acts an model method used
        to create CustomResourceDefinitions

        Args:
            object_name (str): name of the custom object

        Returns:
            str: custom object
        """
        self.api_version =api_version
        self.kind = kind
        self.object_name = object_name
# Creating catalog source body
        catalog_source_body = client.V1CustomResourceDefinition(api_version='operators.coreos.com/v1alpha1',
        kind='CatalogSource',
        metadata=client.V1ObjectMeta(name='openshift-builds-operator'),
        spec={"displayName":'openshift-builds-operator',
                "image": 'quay.io/jkhelil/openshift-builds-operator-bundle-index:v0.11.0',
                "publisher": "Red Hat",
                "sourceType": 'grpc',
                "updateStrategy":{
                    "registryPoll":{"interval": "15m"}
                }
        })

# # Creating subscription body
        subscription_body = client.V1CustomResourceDefinition(api_version='operators.coreos.com/v1alpha1',
        kind='Subscription',
        metadata=client.V1ObjectMeta(name='openshift-builds-operator'),
        spec={"channel": 'alpha',
            "installPlanApproval": 'Automatic',
            "name": 'openshift-builds-operator',
            "source": 'openshift-builds-operator',
            "sourceNamespace": 'openshift-marketplace',
            "startingCSV": 'openshift-builds-operator.v0.11.0'
        })
        custobjapi = client.CustomObjectsApi()
        try:
            custobjapi.create_cluster_custom_object(group='operators.coreos.com', version='v1alpha1', plural='catalogsource', body=catalog_source_body)
        except ApiException as ex:
            if not ex.status == 201:
                raise

        # if self.kind == "CatalogSource":
        #     body = catalog_source_body
        #     plural='catalogsource'
        #     try:
        #         custobjapi.create_cluster_custom_object(group='operators.coreos.com', version='v1alpha1', plural='catalogsource', body=catalog_source_body)
        #     except ApiException as ex:
        #         if not ex.status == 201:
        #             raise
        # elif self.kind == "Subscription":
        #     body = subscription_body
        #     plural='subscription'
        #     try:
        #         custobjapi.create_cluster_custom_object(group='operators.coreos.com', version='v1alpha1', plural='subs', body=subscription_body)
        #     except ApiException as ex:
        #         if not ex.status == 201:
        #             raise