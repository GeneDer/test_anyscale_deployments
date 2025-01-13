#./set_up_aica_release_test_service.sh -i localhost:5555/anyscale/endpoints_aica:1.0.0-8335 --start_args "--model-id meta-llama/Meta-Llama-3-8B-Instruct --gpu-type A10 --tensor-parallelism 1"
#!/bin/bash
set -exuo pipefail

# Initialize variables
image_tagged_name=""
start_args=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i)
      image_tagged_name="$2"
      shift 2
      ;;
    --start_args)
      shift
      start_args="$*"
      break
      ;;
    *)
      echo "ERROR: unknown argument passed: $1"
      exit 1
      ;;
  esac
done

# Print the extracted values (for debugging purposes)
echo "Image Tagged Name: ${image_tagged_name}"
echo "Start Args: ${start_args}"

ANYSCALE_HOST="https://ci-b62a17.anyscale-dev.dev"
export ANYSCALE_HOST

set +x
ANYSCALE_CLI_TOKEN="ath0_CkgwRgIhAIOV0hInnuOsszvlSN35ZNE3yYJJMW_umU8i73wTi2zvAiEA_2XxqqnqXx6UJX8G3aQx_lubICQG8BH7eRtAnfXPzcMSYRIgA919kUA2b0Kc4tjeJOmQ0a-_wcaaj9zwNxagMQ2O2MYiHnVzcl92ZXNiOWdnYmJrdmNuNzI4cGNmcmZkbGdjYToMCLmlrZgSEPjViJ4DQgwIjefMuAYQ-NWIngPyAQA"
export ANYSCALE_CLI_TOKEN
set -x

# Suppress the output of the aws s3 cp command
set +x
HF_TOKEN="REDACTED"
export HF_TOKEN
set -x

set +x
service_url=$(python set_up_aica_release_test_service.py \
    -i "${image_tagged_name}" \
    --start_args "${start_args} \
    --hf-token ${HF_TOKEN}"
)
set -x
