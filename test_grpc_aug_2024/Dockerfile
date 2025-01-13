# docker build . -t geneanyscale/gene-test-anyscale:grpc_aug_2024
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:grpc_aug_2024 bash
# docker push geneanyscale/gene-test-anyscale:grpc_aug_2024

# Use Anyscale base image
FROM anyscale/ray:2.34.0-py311

WORKDIR /home/ray

# Copy Protobuf and deployment definitions into the Docker image
COPY user_defined_protos.proto /home/ray/user_defined_protos.proto
COPY deployment.py /home/ray/deployment.py

# Add working directory into Python path so any nodes can import them
ENV PYTHONPATH=/home/ray

# Build Python code from .proto file
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. ./user_defined_protos.proto
