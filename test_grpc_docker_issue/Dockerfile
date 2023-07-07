FROM python:3.10.11
# Install libraries and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends

WORKDIR /src

COPY requirements.txt /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src

WORKDIR /src

# CMD [ "ray", "start", "--head", "--port=6379", "--redis-shard-ports=6380,6381", "--object-manager-port=22345","--node-manager-port=22346","--dashboard-host=0.0.0.0","--block"]
# ENTRYPOINT ["serve", "start", "--http-host", "0.0.0.0"] # this doesn't start a ray cluster
ENTRYPOINT ["serve", "run", "--host", "0.0.0.0", "serve_agent:agent"]
