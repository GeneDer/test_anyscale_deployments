# Use the latest Ray GPU image, `rayproject/ray:latest-py38-gpu`, so the Whisper model can run on GPUs.
FROM rayproject/ray:latest-py38-gpu

# Install the package `faster_whisper`, which is a dependency for the Whisper model.
RUN pip install faster_whisper==0.10.0
RUN sudo apt-get update && sudo apt-get install curl -y

# Download the source code for the Whisper application into `whisper_example.py`.
RUN curl -O https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/doc_code/whisper_example.py

