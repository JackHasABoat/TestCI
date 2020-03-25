FROM docker.io/centos:7

RUN yum -y install yum-plugin-fastestmirror epel-release

RUN yum -y update; yum -y install \
    bind-utils \
    nc \
    net-tools \
    openssl \
    python36 \
    python36-libs \
    python36-pip \
    python36-PyYAML \
    wget \
    which \
    && yum --enablerepo=* clean all \
    && rm -rf /var/cache/yum

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY myapp /app
ENV PYTHONPATH /app/myapp:$PYTHONPATH

ENV FLASK_APP myapp/api.py
CMD flask run
