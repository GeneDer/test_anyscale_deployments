# pull base image
FROM rayproject/ray-deps:latest

# set work directory
WORKDIR /ray

# Setup bazel
RUN sudo apt-get update
RUN sudo apt-get install -y build-essential curl gcc-9 g++-9 pkg-config psmisc unzip git
RUN sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 \
              --slave /usr/bin/g++ g++ /usr/bin/g++-9 \
              --slave /usr/bin/gcov gcov /usr/bin/gcov-9

COPY . /ray
RUN ./ci/env/install-bazel.sh --system
RUN PATH=$PATH:/home/ray/bin

# Setup node
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN echo hello_world
# RUN echo "$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
# ENV NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
# ENV NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
# RUN [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
# RUN nvm install 14
# RUN nvm use 14
#
# # Build dashboard
# RUN cd dashboard/client
# RUN npm ci
# RUN npm run build
#
# # Build ray
# RUN cd ../..
RUN pip install --upgrade pip
RUN pip install -r python/requirements.txt
RUN bazel info
RUN bazel build //:ray_pkg
RUN pip install -e python

# Expose ports
EXPOSE 8000
EXPOSE 8265


# FROM rayproject/ray-deps:latest
#
# # Install dependencies needed to build ray
# RUN sudo apt-get update && sudo apt-get install -y curl unzip cmake gcc g++ && sudo apt-get clean
# WORKDIR /ray
# COPY . /ray
# RUN ./ci/env/install-bazel.sh --system
# ENV PATH=$PATH:/home/ray/bin
# RUN echo 'build --remote_upload_local_results=false' >> $HOME/.bazelrc
# WORKDIR /ray/
# # The result of bazel build is reused in pip install. It if run first to allow
# # for failover to serial build if parallel build requires too much resources.
# # RUN bazel build //:ray_pkg || bazel build --jobs 1 //:ray_pkg
# WORKDIR /ray/python/
# RUN pip install -e .
# WORKDIR /ray


# FROM ubuntu:20.04
#
# RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
# 	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
# ENV LANG="en_US.utf8"
# ENV TZ="America/Los_Angeles"
# ENV DEBIAN_FRONTEND="noninteractive"
#
# RUN apt-get update
# RUN apt-get install -y curl unzip cmake gcc g++ git
# RUN apt-get clean
#
# WORKDIR /ray
#
# COPY . /ray
# RUN ci/env/install-bazel.sh
# RUN export PATH=$HOME/bin:$PATH
