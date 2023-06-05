Feature: As a user of Openshift Build:v2 Operator
            I want to test if Openshift Build:v2 operator is deployed on operator hub properly
            If we need to install an operator manually using the cli we need the below
                - ensure your catalog source is installed
                - create an OperatorGroup
                - create the Subscription object

  Scenario: Deploy Openshift Build:v2 Operator on operator hub
    Given the Kubernetes cluster is available
    When the following "CustomResourceDefinition" are created:
    |kind         | name                      |api_version                  |
    |CatalogSource| openshift-builds-operator |operators.coreos.com/v1alpha1|
    |Subscription | openshift-builds-operator |operators.coreos.com/v1alpha1|
    Then we check the status of "CustomResourceDefinition":
    |kind         | name                              |
    |CatalogSource| openshift-builds-operator         |
    |Subscription | openshift-builds-operator         |
    |CSV          | openshift-builds-operator.v0.11.0 |
    And we check for the operator pod status in "openshift-marketplace" project