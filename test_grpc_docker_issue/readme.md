

```
docker build . -t rl-agent:test
docker build . -t rl-agent:latest

docker run -it --rm -p 8000:8000 rl-agent:test bash
docker run -it --rm -p 8000:8000 rl-agent:latest

docker run -it --rm -v /Users/gene/workspace/test_anyscale_deployments/test_grpc_docker_issue:/src -w /src -p 8000:8000 rl-agent:test bash


```