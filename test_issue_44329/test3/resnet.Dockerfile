# Use the latest Ray CPU image, `rayproject/ray:latest-py38-cpu`.
FROM rayproject/ray:latest-py38-cpu

# Install the packages `torch` and `torchvision`, which are dependencies for the ResNet model.
RUN torch==2.0.1 torchvision==0.15.2
RUN sudo apt-get update && sudo apt-get install curl -y

# Download the source code for the ResNet application into `resnet50_example.py`.
RUN curl -O https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/doc_code/resnet50_example.py

