# docker build . -t geneanyscale/gene-test-anyscale:import_issue__docker_2_10_0_5
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:import_issue__docker_2_10_0_5 bash
# docker push geneanyscale/gene-test-anyscale:import_issue__docker_2_10_0_5
FROM rayproject/ray:2.10.0-py310

# FROM rayproject/ray:latest-py310-cpu
RUN pip install Faker==18.13.0
# WORKDIR /serve_app
COPY fake.py /home/ray/fake.py

# ENV PYTHONPATH=/serve_app
