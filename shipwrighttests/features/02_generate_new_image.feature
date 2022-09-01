Feature: Build container images for nodejs app using "buildpacks-v3" and "clusterbuildstrategies"
    Validate building of container image for a nodejs app using "buildpacks-v3" 
    and "clusterbuildstrategies" and pushing the image to a container registry.

Scenario: Build container images for nodejs app using buildpacks-v3
Given The following "clusterbuildstrategies.shipwright.io" objects are present:
       | name            |
       | buildah         |
       | buildkit        |
       | buildpacks-v3   |
       | kaniko          |
       | ko              |
       | source-to-image |
Then the user generates a secret to access our container registry, such as one on Docker Hub or Quay.io:
And the user creates a custom build object
And the user creates a buildrun for the build