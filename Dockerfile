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
Run mkdir /app/myapp
COPY requirements.txt /app/requirements.txt
WORKDIR /app/myapp
RUN pip3.6 install -r requirements.txt
COPY myapp /app/myapp

ENV PYTHONPATH /app/myapp:$PYTHONPATH
ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV FLASK_APP api.py
CMD flask run --host 0.0.0.0
