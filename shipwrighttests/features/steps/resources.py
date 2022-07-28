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
        