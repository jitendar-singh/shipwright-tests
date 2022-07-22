Feature: Assert Shipwright Installation

    Assert the installation of Shipwright and its dependencies in the Kubernetes cluster.

    Scenario: Asserting Shipwright Installation
        Given the Kubernetes cluster is available
        Then "tekton-pipelines-controller" is deployed and "READY" on "tekton-pipelines" namespace
        And "tekton-pipelines-webhook" is deployed and "READY" on "tekton-pipelines" namespace
        And "shipwright-build-controller" is deployed and "READY" on "shipwright-build" namespace
        Then the following resource names belong to "shipwright.io/v1alpha1" API version:
            | resource_name          | scope      |
            | buildruns              | Namespaced |
            | builds                 | Namespaced |
            | buildstrategies        | Namespaced |
            | clusterbuildstrategies | Cluster    |
        And the following "clusterbuildstrategies.shipwright.io" objects are present:
            | name            |
            | buildah         |
            | buildkit        |
            | buildpacks-v3   |
            | kaniko          |
            | ko              |
            | source-to-image |
