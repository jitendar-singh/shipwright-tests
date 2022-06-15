#!/bin/sh

#-----------------------------------------------------------------------------
# Global Variables
#-----------------------------------------------------------------------------
export V_FLAG=-v
OUTPUT_DIR="$(pwd)"/_output
export OUTPUT_DIR
export LOGS_DIR="${OUTPUT_DIR}"/logs
export GOLANGCI_LINT_BIN="${OUTPUT_DIR}"/golangci-lint
export PYTHON_VENV_DIR="${OUTPUT_DIR}"/venv3
# -- Variables for system tests
export TEST_SYSTEM_ARTIFACTS=/tmp/artifacts

# -- Setting up the venv
python3 -m venv "${PYTHON_VENV_DIR}"
"${PYTHON_VENV_DIR}"/bin/pip install --upgrade setuptools
"${PYTHON_VENV_DIR}"/bin/pip install --upgrade pip
# -- Generating a new namespace name
echo "test-namespace-$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 8)" > "${OUTPUT_DIR}"/test-namespace

TEST_NAMESPACE=$(cat "${OUTPUT_DIR}"/test-namespace)
export TEST_NAMESPACE
echo "Assigning value to variable TEST_NAMESPACE=${TEST_NAMESPACE}"
# -- create namespace
echo "Creating namespace"
kubectl delete namespace "${TEST_NAMESPACE}" --timeout=45s --wait
kubectl create namespace "${TEST_NAMESPACE}"

mkdir -p "${LOGS_DIR}"/system-tests-logs
mkdir -p "${OUTPUT_DIR}"/system-tests-output
touch "${OUTPUT_DIR}"/backups.txt
TEST_SYSTEM_OUTPUT_DIR="${OUTPUT_DIR}"/system
export TEST_SYSTEM_OUTPUT_DIR
echo "Logs directory created at ""${LOGS_DIR}"/system

# -- Setting the project
kubectl config set-context --current --namespace="${TEST_NAMESPACE}"

# -- Trigger the test
echo "Environment setup in progress"
"${PYTHON_VENV_DIR}"/bin/pip install -q -r shipwrighttests/requirements.txt
echo "Running tests in namespace with TEST_NAMESPACE=${TEST_NAMESPACE}"
echo "Logs will be collected in ""${TEST_SYSTEM_OUTPUT_DIR}"
"${PYTHON_VENV_DIR}"/bin/behave --junit --junit-directory "${TEST_SYSTEM_OUTPUT_DIR}" \
                              --no-capture --no-capture-stderr \
                              ./shipwrighttests/features -D project_name="${TEST_NAMESPACE}"                      
echo "Test run logs collected in ""${TEST_SYSTEM_OUTPUT_DIR}"