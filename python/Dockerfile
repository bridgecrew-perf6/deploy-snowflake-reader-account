FROM python:latest

COPY /src/deploy_reader.py .
COPY config.json .

RUN  pip install snowflake-connector-python

ENTRYPOINT [ "python" ]

CMD [ "--version" ]