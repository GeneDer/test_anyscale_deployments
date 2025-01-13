import argparse
import logging
import os
import subprocess
from typing import Dict

import anyscale
import yaml
from anyscale.service.models import ServiceConfig, ServiceState

AICA_RELEASE_TEST_COMPUTE_CONFIG_NAME = "endpoints-aica-release-test-aviary-staging"
AICA_RELEASE_TEST_SERVICE_NAME = "test_rayllm_direct_ingress"

logger = logging.getLogger(__file__)
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

_AVIARY_CLOUD = "anyscale_v2_default_cloud"


def read_serve_config(file_path: str) -> Dict:
    if not file_path.endswith(".yaml"):
        raise RuntimeError(
            "Must pass in a Serve config yaml file using the -f option. Got "
            f'file path "{file_path}", which does not end in ".yaml".'
        )
    if not os.path.exists(file_path):
        raise RuntimeError(f"File path {file_path} does not exist.")

    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def create_service(image_name: str, application_config: Dict):
    """Creates a service."""

    service_config = ServiceConfig(
        name=AICA_RELEASE_TEST_SERVICE_NAME,
        image_uri=image_name,
        applications=[application_config],
        query_auth_token_enabled=False,
        compute_config=AICA_RELEASE_TEST_COMPUTE_CONFIG_NAME,
    )

    # If the service already exists, apply a rollout with canary_percent 100,
    # so the new service starts immediately. Otherwise, start a new service
    # without a canary_percent.
    try:
        status = anyscale.service.status(name=AICA_RELEASE_TEST_SERVICE_NAME)
        if status.state == ServiceState.TERMINATED:
            canary_percent = None
            logger.info(
                f"Service with name {AICA_RELEASE_TEST_SERVICE_NAME} is "
                "currently terminated. Starting a new service."
            )
        else:
            canary_percent = 100
            logger.info(
                f"Service with name {AICA_RELEASE_TEST_SERVICE_NAME} is "
                "currently running. Rolling out with canary-percent 100."
            )
    except RuntimeError:
        canary_percent = None
        logger.info(
            f"Service with name {AICA_RELEASE_TEST_SERVICE_NAME} has "
            "never been run. Starting a new service."
        )

    anyscale.service.deploy(config=service_config, canary_percent=canary_percent)

    # Wait for the service to start running.
    anyscale.service.wait(
        AICA_RELEASE_TEST_SERVICE_NAME,
        cloud=_AVIARY_CLOUD,
        state=ServiceState.RUNNING,
        timeout_s=1200,
    )


def print_service_url():
    """Prints the serivce's query URL.
    This lets the bash script read the URL and save it.
    """

    status = anyscale.service.status(
        name=AICA_RELEASE_TEST_SERVICE_NAME, cloud=_AVIARY_CLOUD
    )
    print(status.query_url)


def _find_latest_yaml(directory):
    # List to store matched files
    matched_files = []

    # Iterate through the files in the given directory
    for filename in os.listdir(directory):
        if filename.startswith("serve_") and filename.endswith(".yaml"):
            matched_files.append(filename)

    if not matched_files:
        return None

    # Find the file with the latest timestamp by sorting the filenames
    latest_file = max(matched_files)

    return os.path.join(directory, latest_file)


def _generate_config(start_args: str):
    # Directory to check
    directory_path = "/tmp/templates_repo/templates"

    # Check if the directory exists
    directory_exists = os.path.exists(directory_path) and os.path.isdir(directory_path)
    if not directory_exists:
        print(f"Directory {directory_path} doesn't exist.")

    command = ["rayllm", "gen-config"] + start_args.split()

    # Run the command and wait for it to complete
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode != 0:
        print(
            f'Command "{command}" failed with return code {result.returncode}.\n\n'
            f"Command output: {result.stdout}\n\n"
            f"Command error: {result.stderr}\n\n"
        )
        return None

    # Find the latest YAML file in the current directory
    return _find_latest_yaml(".")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--image_name",
        type=str,
        required=True,
        default="The Docker image to use when running the service.",
    )
    parser.add_argument(
        "--start_args",
        type=str,
        required=True,
        default="The arguments to pass to the rayllm start script.",
    )
    args = parser.parse_args()

    start_args = args.start_args
    serve_config_path = _generate_config(start_args)

    serve_config = read_serve_config(serve_config_path)
    application_config = serve_config["applications"][0]

    # Converts the inlined file path to the underlying model config
    for model_key in application_config["args"]:
        for idx, model_list_val in enumerate(application_config["args"][model_key]):
            if os.path.isfile(model_list_val):
                with open(model_list_val, "r") as f:
                    application_config["args"][model_key][idx] = yaml.safe_load(f)

    create_service(image_name=args.image_name, application_config=application_config)
    print_service_url()
