### Setup 
1. Install docker


```


```


### Run 
```
docker run -it --rm -v $(pwd):/app -w /app python:3.9.0-alpine sh
docker run -it --rm -v /Users/gene/workspace/ray:/ray -w /ray python:3.9.0-alpine sh
foo


docker run -it --rm -v /Users/gene/workspace/ray:/ray -w /ray rayproject/ray-deps:latest bash

docker run -it --rm -v /Users/gene/workspace/ray:/ray -w /ray ubuntu:20.04 bash


docker build -t gene-ray-dev:latest .
docker build -t gene-ray-dev:latest -f Dockerfile /Users/gene/workspace/ray

```