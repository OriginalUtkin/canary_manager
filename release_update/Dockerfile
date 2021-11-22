ARG BASE_IMAGE

FROM ${BASE_IMAGE}

COPY . /release_update
WORKDIR /release_update

RUN pip install --ignore-installed -r requirements/requirements.txt
RUN chmod +x release_update/main.py

CMD ["./release_update/main.py"]
