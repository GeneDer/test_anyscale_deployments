# docker build . -t geneanyscale/gene-test-anyscale:test-rayllm
# docker run -it --rm -p 8265:8265 --shm-size=10.04gb geneanyscale/gene-test-anyscale:test-rayllm
# docker push geneanyscale/gene-test-anyscale:test-rayllm

# Use Anyscale base image
FROM 830883877497.dkr.ecr.us-west-2.amazonaws.com/anyscale/runtime:2.43.0.69d022-py311-cu123-as

RUN pip install vllm==0.7.2 xgrammar==0.1.11 pynvml==12.0.0 asyncache>=0.3.1 httpx>=0.27.2 jsonref>=1.1.0

# Override runtime.
ENV ANYSCALE_DISABLE_OPTIMIZED_RAY=true
