Shipwright Tests
----------------

# What's Shipwright?

Shipwright provide developers a simplified approach to build container images with minimal settings and without previous knowledge about containers. All you need is your Git repository with  your source code and a container registry to store the results.

# Running Tests Locally

In order to run this project locally, you need to have Python 3.10 installed, and then let's start by installing the project dependencies in the Virtual-Environment (by default under `venv` directory):

```bash
make pip-install
```

With the dependencies in place, run the unit-tests against the steps with the following:

```bash
make test
```

And finally, run the Shipwright behavior driven tests with:

```bash
make behave
```
	