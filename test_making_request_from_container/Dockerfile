# docker build . -t geneanyscale/gene-test-anyscale:request_from_outside_container
# docker run -it --rm -p 8000:8000 geneanyscale/gene-test-anyscale:request_from_outside_container bash
# docker push geneanyscale/gene-test-anyscale:request_from_outside_container

# docker build . -t test_request_from_outside_container:latest
# docker run -it --rm -p 8000:8000 test_request_from_outside_container:latest
FROM rayproject/ray:2.10.0-py310

RUN pip install Faker==18.13.0

COPY fake.py /home/ray/fake.py

EXPOSE 8000

CMD ["sh", "-c", "ray start --head --dashboard-host 0.0.0.0 && serve run fake:app"]
