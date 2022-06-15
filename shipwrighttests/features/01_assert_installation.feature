Feature: Assert Shipwright Installation

	Assert the installation of Shipwright and its dependencies in the Kubernetes cluster.
	With Shipwright, developers get a simplified approach for building container images, by defining 
    a minimal YAML that does not require any previous knowledge of containers or container tooling. 
    All you need is your source code in git and access to a container registry.
	

	Scenario: Asserting Shipwright Installation
        Given the Kubernetes cluster is available
		Then "tekton-pipelines-controller" is deployed and "READY" on "tekton-pipelines" namespace
		And "tekton-pipelines-webhook" is deployed and "READY" on "tekton-pipelines" namespace
        And we check namespace/shipwright-build should be created
		Then we check that the following resources are created
        | resource           | resource_name                        |
		| role               | shipwright-build-controller          |
		| clusterrole        | shipwright-build-controller          |
		| clusterrolebinding | shipwright-build-controller          |
		| rolebinding        | shipwright-build-controller          |
        | serviceaccount     | shipwright-build-controller          |
        | deployment         | shipwright-build-controller          |
		| crd                | buildruns.shipwright.io              |
		| crd                | builds.shipwright.io                 |
		| crd                | buildstrategies.shipwright.io        |
		| crd                | clusterbuildstrategies.shipwright.io |
		And "shipwright-build-controller" is deployed and "READY" on "shipwright-build" namespace
        And check the following clusterbuildstrategy.shipwright.io/ are installed
        | clusterbuildstrategy     |
        | buildkit                 |
        | buildkit-v3              |
        | buildpacks-v3-heroku     |
        | kaniko                   |
        | kaniko-trivy             |
        | ko                       |
        | source-to-image-redhat   |
        | source-to-image          |
