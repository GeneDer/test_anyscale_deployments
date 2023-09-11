# docker build . -t geneanyscale/gene-test-anyscale:latest
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:latest bash
# docker push geneanyscale/gene-test-anyscale:latest


# Use Anyscale base image
FROM anyscale/ray:nightly-py310

# Install dependencies
RUN pip install --upgrade pip && pip install -U torch==2.0.1 torchvision==0.15.2

WORKDIR /home/ray

# Copy local code including protobuf and service definitions into docker image
COPY . /home/ray

# Add working directory into python path so they are importable
ENV PYTHONPATH=/home/ray
