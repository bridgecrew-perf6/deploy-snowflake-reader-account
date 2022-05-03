FROM amazonlinux:latest AS get_package

RUN curl -o snowsql-1.2.14-linux_x86_64.bash https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.14-linux_x86_64.bash

FROM amazonlinux:latest

RUN yum install -y \
    tar \
    gzip \
    unzip 

ENV SNOWSQL_DEST=/bin 
ENV SNOWSQL_LOGIN_SHELL=/.profile

RUN touch /.profile

COPY --from=get_package snowsql-1.2.14-linux_x86_64.bash .

RUN bash snowsql-1.2.14-linux_x86_64.bash

RUN rm snowsql-1.2.14-linux_x86_64.bash

COPY /src/ .
COPY config /root/.snowsql/config

ENTRYPOINT [ "snowsql" ]

CMD [ "--version" ]