

```
docker build . -t rl-agent:test
docker build . -t rl-agent:latest

docker run -it --rm -p 8000:8000 rl-agent:test bash
docker run -it --rm -p 8000:8000 rl-agent:latest

docker run -it --rm -v /Users/gene/workspace/test_anyscale_deployments/test_grpc_docker_issue:/src -w /src -p 8000:8000 rl-agent:test bash


docker run -it --rm -p 8000:8000 -p 8265:8265 rl-agent:latest
docker run -it --rm -p 8000:8000 -p 8265:8265 rl-agent:latest bash

docker exec -it 63aa09ff4fc1 serve start --http-host "0.0.0.0"
docker exec -it d1075b5740f6 bash
docker exec -it d1075b5740f6 serve run --host 0.0.0.0 serve_agent:agent

ray start --head --port=6379 --redis-shard-ports=6380,6381 --object-manager-port=22345 --node-manager-port=22346 --dashboard-host=0.0.0.0 --block


apt-get install nano
nano /usr/local/lib/python3.10/site-packages/ray/serve/scripts.py


```