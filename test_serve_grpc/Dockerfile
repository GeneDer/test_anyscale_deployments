# docker build . -t geneanyscale/gene-test-anyscale:latest
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:latest bash
# docker push geneanyscale/gene-test-anyscale:latest


# Use Anyscale base image
FROM anyscale/ray:2.6.2-py310

# Install Ray with grpc proxy code
RUN pip uninstall -y ray && \
    pip install -U https://ray-ci-artifact-pr-public.s3.amazonaws.com/72350bd3a4b8d3d9e2831adb421c4610b374f996/tmp/artifacts/.whl/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl

WORKDIR /home/ray

# Copy local code including protobuf and service definitions into docker image
COPY . /home/ray

# Add working directory into python path so they are importable
ENV PYTHONPATH=/home/ray
