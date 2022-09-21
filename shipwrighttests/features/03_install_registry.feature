Feature: As a user of kubernetes we want to store our images in side a custom registry
    Scenario: Install a container image registry on kubernetes cluster

    Given the Kubernetes cluster is available
    Then the user creates a namespace for the registry
    And creates a deployment using the "registry:2" image
    And create a service to expose the service ports on all nodes on the cluster
