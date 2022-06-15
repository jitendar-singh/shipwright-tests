'''
This module is used as a wrapper for kubernetes cli,
one can create the Kubernetes object & use the 
functionalities to check the resources.
'''

import re
import time

from kubernetes import client, config
from pyshould import should
from shipwrighttests.features.steps.command import Command

'''
Kubernetes class provides the blueprint that we need to
interact with the k8s resources 
'''


class Kubernetes(object):
    def __init__(self):
        self.cmd = Command()

    def get_pod_lst(self, namespace):
        return self.get_resource_lst("pods", namespace)

    def get_resource_lst(self, resource_plural, namespace):
        (output, exit_code) = self.cmd.run(f'kubectl get {resource_plural} -n {namespace} -o "jsonpath={{.items['
                                           f'*].metadata.name}}"')
        exit_code | should.be_equal_to(0)
        return output

    def search_item_in_lst(self, lst, search_pattern):
        lst_arr = lst.split(" ")
        for item in lst_arr:
            if re.match(search_pattern, item) is not None:
                print(f"item matched {item}")
                return item
        print("Given item not matched from the list of pods")
        return None

    def search_pod_in_namespace(self, pod_name_pattern, namespace):
        return self.search_resource_in_namespace("pods", pod_name_pattern, namespace)

    def search_resource_in_namespace(self, resource_plural, name_pattern, namespace):
        print(f"Searching for {resource_plural} that matches {name_pattern} in {namespace} namespace")
        lst = self.get_resource_lst(resource_plural, namespace)
        if len(lst) != 0:
            print("Resource list is {}".format(lst))
            return self.search_item_in_lst(lst, name_pattern)
        else:
            print('Resource list is empty under namespace - {}'.format(namespace))
            return None

    def is_resource_in(self, resource_type):
        output, exit_code = self.cmd.run(f'kubectl get {resource_type}')
        return exit_code == 0

    def wait_for_pod(self, pod_name_pattern, namespace, interval=5, timeout=60):
        pod = self.search_pod_in_namespace(pod_name_pattern, namespace)
        start = 0
        if pod is not None:
            return pod
        else:
            while ((start + interval) <= timeout):
                pod = self.search_pod_in_namespace(pod_name_pattern, namespace)
                if pod is not None:
                    return pod
                time.sleep(interval)
                start += interval
        return None

    def check_pod_status(self, pod_name, namespace, wait_for_status="Running"):
        cmd = f'kubectl get pod {pod_name} -n {namespace} -o "jsonpath={{.status.phase}}"'
        status_found, output, exit_status = self.cmd.run_wait_for_status(cmd, wait_for_status)
        return status_found

    def get_pod_status(self, pod_name, namespace):
        cmd = f'kubectl get pod {pod_name} -n {namespace} -o "jsonpath={{.status.phase}}"'
        output, exit_status = self.cmd.run(cmd)
        print(f"Get pod status: {output}, {exit_status}")
        if exit_status == 0:
            return output
        return None

    def kubectl_apply(self, yaml):
        (output, exit_code) = self.cmd.run("kubectl apply -f -", yaml)
        return output
    
    def kubectl_create_from_yaml(self, yaml):
        cmd = f'kubectl create -f {yaml}'
        output, exit_status = self.cmd.run(cmd)
        print(f"starting: {output}, {exit_status}")
        if exit_status == 0:
            return output
        return None

    def get_configmap(self, namespace):
        output, exit_code = self.cmd.run(f'kubectl get cm -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def get_deploymentconfig(self, namespace):
        output, exit_code = self.cmd.run(f'kubectl get dc -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def get_service(self, namespace):
        output, exit_code = self.cmd.run(f'kubectl get svc -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def get_service_account(self, namespace):
        output, exit_code = self.cmd.run(f'kubectl get sa -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def get_role_binding(self, namespace):
        output, exit_code = self.cmd.run(f'kubectl get rolebinding -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def get_route(self, route_name, namespace):
        output, exit_code = self.cmd.run(f'kubectl get route {route_name} -n {namespace}')
        exit_code | should.be_equal_to(0)
        return output

    def expose_service_route(self, service_name, namespace):
        output, exit_code = self.cmd.run(f'kubectl expose svc/{service_name} -n {namespace} --name={service_name}')
        return re.search(r'.*%s\sexposed' % service_name, output)

    def get_route_host(self, name, namespace):
        (output, exit_code) = self.cmd.run(
            f'kubectl get route {name} -n {namespace} -o "jsonpath={{.status.ingress[0].host}}"')
        exit_code | should.be_equal_to(0)
        return output

    def check_for_deployment_status(self, deployment_name, namespace, wait_for_status="True"):
        deployment_status_cmd = f'kubectl get deployment {deployment_name} -n {namespace} -o "jsonpath={{' \
                                f'.status.conditions[*].status}}" '
        deployment_status, exit_code = self.cmd.run_wait_for_status(deployment_status_cmd, wait_for_status, 5, 600)
        exit_code | should.be_equal_to(0)
        return deployment_status

    def check_for_deployment_config_status(self, dc_name, namespace, wait_for="condition=Available"):
        output, exit_code = self.cmd.run_wait_for('dc', 'jenkins', wait_for, timeout_seconds=600)
        if exit_code != 0:
            print(output)
        return output, exit_code

    def set_env_for_deployment_config(self, name, namespace, key, value):
        env_cmd = f'kubectl -n {namespace} set env dc/{name} {key}={value}'
        print( "kubectl set command: {}".format(env_cmd))
        output, exit_code = self.cmd.run(env_cmd)
        exit_code | should.be_equal_to(0)
        time.sleep(3)
        return  output, exit_code

    def get_deployment_env_info(self, name, namespace):
        env_cmd = f'kubectl get deploy {name} -n {namespace} -o "jsonpath={{.spec.template.spec.containers[0].env}}"'
        env, exit_code = self.cmd.run(env_cmd)
        exit_code | should.be_equal_to(0)
        return env

    def get_deployment_envFrom_info(self, name, namespace):
        env_from_cmd = f'kubectl get deploy {name} -n {namespace} -o "jsonpath={{.spec.template.spec.containers[0].envFrom}}"'
        env_from, exit_code = self.cmd.run(env_from_cmd)
        exit_code | should.be_equal_to(0)
        return env_from

    def get_resource_info_by_jsonpath(self, resource_type, name, namespace, json_path, wait=False):
        output, exit_code = self.cmd.run(f'kubectl get {resource_type} {name} -n {namespace} -o "jsonpath={json_path}"')
        if exit_code != 0:
            if wait:
                attempts = 5
                while exit_code != 0 and attempts > 0:
                    output, exit_code = self.cmd.run(
                        f'kubectl get {resource_type} {name} -n {namespace} -o "jsonpath={json_path}"')
                    attempts -= 1
                    time.sleep(5)
        exit_code | should.be_equal_to(0).desc(f'Exit code should be 0:\n OUTPUT:\n{output}')
        return output

    def get_resource_info_by_jq(self, resource_type, name, namespace, jq_expression, wait=False):
        output, exit_code = self.cmd.run(
            f'kubectl get {resource_type} {name} -n {namespace} -o json | jq -rc \'{jq_expression}\'')
        if exit_code != 0:
            if wait:
                attempts = 5
                while exit_code != 0 and attempts > 0:
                    output, exit_code = self.cmd.run(
                        f'kubectl get {resource_type} {name} -n {namespace} -o json | jq -rc \'{jq_expression}\'')
                    attempts -= 1
                    time.sleep(5)
        exit_code | should.be_equal_to(0).desc(f'Exit code should be 0:\n OUTPUT:\n{output}')
        return output.rstrip("\n")
    
    def delete(self,resource_type: str,resource: str, namespace: str):
        '''
        Delete resources in a specific namespace
        '''
        cmd = f'kubectl delete {resource_type} {resource} -n {namespace}'
        output, exit_status = self.cmd.run(cmd)
        print(f"{output}")
        if exit_status == 0:
            return output
        return None