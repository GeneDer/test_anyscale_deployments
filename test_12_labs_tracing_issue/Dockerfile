# docker build . -t geneanyscale/gene-test-anyscale:12_labs_tracing_issue2
# docker push geneanyscale/gene-test-anyscale:12_labs_tracing_issue2


# Use Anyscale base image
FROM anyscale/ray:2.40.0-slim-py310

# Copy the requirements file into the Docker image
COPY requirements.txt .

# Install all dependencies specified in requirements.txt
RUN pip install --no-cache-dir  --no-dependencies -r requirements.txt

# Copy exporter file and application definitions into the Docker image
COPY serve_call_external_service.py /home/ray/serve_call_external_service.py
COPY simple_app.py /home/ray/simple_app.py
COPY app_tracing.py /home/ray/exporter.py

# Add working directory into python path so they are importable
ENV PYTHONPATH=/home/ray
