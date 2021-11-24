ARG BASE_IMAGE

FROM ${BASE_IMAGE}

COPY . /tools
WORKDIR /tools

RUN pip install --ignore-installed -r requirements/requirements.txt

RUN chmod +x main.py
RUN chmod +x release_update_main.py
