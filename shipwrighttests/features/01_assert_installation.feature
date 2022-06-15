Feature: Assert Shipwright Instalation

	Assert the installation of Shipwright and its dependencies in the Kubernetes cluster

	Scenario: Asserting Shipwright Installation
		Given the Kubernetes cluster is available
		Then "tekton-pipelines-controller" is deployed and "READY" on "tekton-pipelines" namespace
		And "tekton-pipelines-webhook" is deployed and "READY" on "tekton-pipelines" namespace
		And "shipwright-build-controller" is deployed and "READY" on "shipwright-build" namespace
