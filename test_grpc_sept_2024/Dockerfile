# docker build . -t geneanyscale/gene-test-anyscale:grpc-gcp-test-2024

# Use Anyscale base image
FROM anyscale/ray:2.37.0-py310

WORKDIR /home/ray

# Copy protobuf and deployment definitions into the Docker image
COPY user_defined_protos.proto /home/ray/user_defined_protos.proto
COPY deployment.py /home/ray/deployment.py

# Add working directory into Python path so any nodes can import them
ENV PYTHONPATH=/home/ray

RUN pip install --upgrade protobuf

# Build Python code from .proto file
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. ./user_defined_protos.proto
