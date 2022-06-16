import pytest

from shipwrighttests.features.steps.install_steps import probe_cluster_available

def test_probe_cluster_available():
	assert probe_cluster_available