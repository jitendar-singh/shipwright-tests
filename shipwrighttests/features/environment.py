from kubernetes import client, config
from kubernetes.client import configuration
from kubernetes.config import ConfigException




def before_all(_context):
    '''
        before_step(context, step), after_step(context, step)
            These run before and after every step.
            The step passed in is an instance of Step.
        before_feature(context, feature), after_feature(context, feature)
            These run before and after each feature file is exercised.
            The feature passed in is an instance of Feature.
        before_all(context), after_all(context)
            These run before and after the whole shooting match.
        before_scenario(context, scenario), after_scenario(context, scenario)
            These run before and after each scenario is run.
            The scenario passed in is an instance of Scenario.
    '''
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

