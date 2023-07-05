FROM python:3.10.11
# Install libraries and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends

WORKDIR /src

COPY requirements.txt /src
RUN pip3 install -r requirements.txt

COPY . /src

WORKDIR /src

CMD ["serve", "run", "-h", "0.0.0.0", "serve_agent:agent"]

