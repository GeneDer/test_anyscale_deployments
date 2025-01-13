# docker build . -t geneanyscale/gene-test-anyscale:grpc-gcp-test
# docker run -it --rm -p 8265:8265 --shm-size=10.04gb geneanyscale/gene-test-anyscale:grpc-gcp-test bash
# docker push geneanyscale/gene-test-anyscale:grpc-gcp-test

# Use Anyscale base image
FROM anyscale/ray:2.36.0-py310

WORKDIR /home/ray

# Copy Protobuf and deployment definitions into the Docker image
COPY user_defined_protos.proto /home/ray/user_defined_protos.proto
COPY deployment.py /home/ray/deployment.py

# Add working directory into Python path so any nodes can import them
ENV PYTHONPATH=/home/ray

# Build Python code from .proto file
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. ./user_defined_protos.proto

# Override runtime.
ENV ANYSCALE_DISABLE_OPTIMIZED_RAY=true
COPY ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl /home/ray/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl
#COPY ../config.yaml /home/ray/runtime/config.yaml
#ADD runtime /home/ray/runtime
#RUN cd /home/ray/runtime && bazel build //:ray_pkg
RUN pip --no-cache-dir install /home/ray/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl

# Add cret.
# Ref: https://bbengfort.github.io/2017/03/secure-grpc/
#ENV RAY_SERVE_GRPC_SERVER_CERT=/home/ray/server.crt
#COPY server.crt $RAY_SERVE_GRPC_SERVER_CERT
#ENV RAY_SERVE_GRPC_SERVER_KEY=/home/ray/server.key
#COPY server.key $RAY_SERVE_GRPC_SERVER_KEY

#RUN sudo chmod +r $RAY_SERVE_GRPC_SERVER_CERT $RAY_SERVE_GRPC_SERVER_KEY
#RUN pip install protobuf==5.26.1
# This might just need to be pip install --upgrade protobuf
#RUN pip install protobuf==5.28.1
RUN pip install --upgrade protobuf

# TODO: add this env from the product
# ENV RAY_SERVE_GRPC_SERVER_USE_SECURE_PORT=1
