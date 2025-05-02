# Overview
This is the publicly available set of Docker images for Anyscale/Ray's Ray Serve LLM and Ray Data LLM projects.

Ray Serve LLM is an LLM serving solution that makes it easy to deploy and manage a variety of open source LLMs.
Ray Data LLM is an offline inferencing solution that makes it easy to run batch inferencing on a variety of open source LLMs.

They do this by:

- Providing an extensive suite of pre-configured open source LLMs, with defaults that work out of the box.
- Supporting Transformer models hosted on Hugging Face Hub, present on local disk, or remote storage.
- Simplifying the deployment of multiple LLMs within a single unified framework.
- Simplifying the addition of new LLMs to within minutes in most cases.
- Offering unique autoscaling support, including scale-to-zero.
- Fully supporting multi-GPU & multi-node model deployments.
- Offering high performance features like continuous batching, quantization and streaming.
- Providing a REST API that is similar to OpenAI's to make it easy to migrate and cross test them.


[Read more here for Ray Serve LLM](https://docs.ray.io/en/latest/serve/llm/overview.html)
[Read more here for Ray Data LLM](https://docs.ray.io/en/latest/data/working-with-llms.html)

## Tags
| Name                 | Notes                                      |
|----------------------|--------------------------------------------|
| :x.xx.x-py311-cu124  | A specific release build                   |
| :nightly-py311-cu124 | Most recently pushed version release image |


## Example
Requires a machine with compatible NVIDIA A10G GPU:

```
# Create container file
cat <<EOF > Dockerfile
FROM anyscale/ray-llm:2.44.0-py311-cu124
EOF

# Create config file
cat <<EOF > service.yaml
name: my-llm-service
containerfile: Dockerfile
applications:
- args:
    llm_configs:
        - model_loading_config:
            model_id: qwen-0.5b
            model_source: Qwen/Qwen2.5-0.5B-Instruct
          accelerator_type: A10G
          deployment_config:
            autoscaling_config:
                min_replicas: 1
                max_replicas: 2
        - model_loading_config:
            model_id: qwen-1.5b
            model_source: Qwen/Qwen2.5-1.5B-Instruct
          accelerator_type: A10G
          deployment_config:
            autoscaling_config:
                min_replicas: 1
                max_replicas: 2
  import_path: ray.serve.llm:build_openai_app
  name: llm_app
  route_prefix: "/"
EOF

anyscale service deploy -f service.yaml

```

# Source
Source is available at [ray/llm/_internal](https://github.com/ray-project/ray/tree/master/python/ray/llm/_internal)
