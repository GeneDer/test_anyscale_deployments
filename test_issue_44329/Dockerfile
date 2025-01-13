# docker build . -t geneanyscale/gene-test-anyscale:import_issue_2_10
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:import_issue_2_10 bash
# docker push geneanyscale/gene-test-anyscale:import_issue_2_10
FROM rayproject/ray:2.10.0-py310


# docker build . -t geneanyscale/gene-test-anyscale:import_issue_2_9_3
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:import_issue_2_9_3 bash
# docker push geneanyscale/gene-test-anyscale:import_issue_2_9_3
# FROM rayproject/ray:2.9.3-py310

ENV WORKING_DIR /home/ray/applications
WORKDIR ${WORKING_DIR}
ADD ./applications/ ${WORKING_DIR}
# ADD ./applications/ /home/ray/applications
COPY worker.py /home/ray/anaconda3/lib/python3.10/site-packages/ray/_private/worker.py
# COPY worker_2_9.py /home/ray/anaconda3/lib/python3.10/site-packages/ray/_private/worker.py
