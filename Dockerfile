ARG BASE_IMAGE

FROM ${BASE_IMAGE}

COPY . /canary_manager
WORKDIR /canary_manager

RUN pip install --ignore-installed -r requirements/requirements.txt
RUN chmod +x main.py

CMD ["./main.py"]
