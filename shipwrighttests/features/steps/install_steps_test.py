import pytest

from shipwrighttests.features.steps.install_steps import probe_cluster_available, probe_deployment_state, probe_cluster_objects, probe_resources_for_apiversion

def test_probe_cluster_available():
	assert probe_cluster_available

def test_probe_deployment_state():
	assert probe_deployment_state

def test_probe_cluster_objects():
	assert probe_cluster_objects

def test_probe_resources_for_apiversion():
	assert probe_resources_for_apiversion