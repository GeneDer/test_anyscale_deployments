# docker build . -t geneanyscale/gene-test-anyscale:triton_test
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:triton_test bash
# docker push geneanyscale/gene-test-anyscale:triton_test

ARG BASE_IMAGE=nvcr.io/nvidia/tritonserver
ARG BASE_IMAGE_TAG=24.04-py3

FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG} as tritonserver-stable-diffusion

# Start of Anyscale modifications
RUN apt-get clean && apt-get update -y
RUN apt-get install -y sudo tzdata supervisor openssh-client openssh-server rsync zip unzip git nfs-common
RUN useradd -ms /bin/bash -d /home/ray ray
RUN usermod -aG sudo ray
RUN echo 'ray ALL=NOPASSWD: ALL' >> /etc/sudoers
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean

# Switch to ray user
USER ray
ENV HOME=/home/ray

RUN sudo apt-get update -y \
    && sudo apt-get install -y python3-venv \
    && sudo rm -rf /var/lib/apt/lists/* \
    && sudo apt-get clean

RUN python3 -m venv --system-site-packages /home/ray/virtualenv
ENV PATH=/home/ray/virtualenv/bin:$PATH

RUN mkdir -p /tmp/ray && mkdir -p /tmp/supervisord

RUN pip install --no-cache-dir anyscale jupyterlab==3.6.1 'urllib3<1.27'
# End of Anyscale modifications
