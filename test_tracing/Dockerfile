# docker build . -t geneanyscale/gene-test-anyscale:test_tracing_multiple_replicas
# docker run -it --rm -p 8265:8265 --shm-size=10.04gb geneanyscale/gene-test-anyscale:serve-direct-ingress bash
# docker push geneanyscale/gene-test-anyscale:test_tracing_multiple_replicas

# Use Anyscale base image
FROM anyscale/ray:2.38.0-slim-py310

# Copy the requirements file into the Docker image
COPY requirements.txt .

# Install all dependencies specified in requirements.txt
RUN pip install --no-cache-dir  --no-dependencies -r requirements.txt

# Copy exporter file and application definitions into the Docker image
COPY exporter.py /home/ray/exporter.py
COPY serve_hello.py /home/ray/serve_hello.py
COPY fp.py /home/ray/fp.py

# Add working directory into python path so they are importable
ENV PYTHONPATH=/home/ray

# Override runtime.
#ENV ANYSCALE_DISABLE_OPTIMIZED_RAY=true
#COPY ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl /home/ray/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl
#COPY ../config.yaml /home/ray/runtime/config.yaml
#ADD runtime /home/ray/runtime
#RUN cd /home/ray/runtime && bazel build //:ray_pkg
#RUN pip --no-cache-dir install /home/ray/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl
