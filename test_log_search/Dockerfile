# docker build . -t geneanyscale/gene-test-anyscale:loki-test
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:loki-test bash
# docker push geneanyscale/gene-test-anyscale:loki-test
# sudo loki -config.file=loki_config.yaml

# Use Anyscale base image
FROM anyscale/ray:nightly-py310

RUN sudo mkdir -p /etc/apt/keyrings/
RUN wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

RUN echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
RUN sudo apt-get update && sudo apt-get install loki

WORKDIR /home/ray

# Copy local code including protobuf and service definitions into docker image
COPY . /home/ray

ENTRYPOINT ["sudo", "loki", "-config.file=loki_config.yaml"]
