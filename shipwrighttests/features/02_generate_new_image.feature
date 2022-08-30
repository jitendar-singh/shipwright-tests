Feature: Build container images for nodejs app using "buildpacks-v3" and "clusterbuildstrategies"
 
 With Shipwright, developers get a simplified approach for building container images, by defining
 a minimal YAML that does not require any previous knowledge of containers or container tooling. 
 All you need is your source code in git and access to a container registry.
 
 Shipwright supports any tool that can build container images in Kubernetes clusters, such as:

 Kaniko
 Cloud Native Buildpacks
 BuildKit
 Buildah

Scenario: Build container images for nodejs app using buildpacks-v3
Given The following "clusterbuildstrategies.shipwright.io" objects are present:
       | name            |
       | buildah         |
       | buildkit        |
       | buildpacks-v3   |
       | kaniko          |
       | ko              |
       | source-to-image |
Then We generate a secret to access our container registry, such as one on Docker Hub or Quay.io:
And We create a custom build object
And We create a buildrun for the build