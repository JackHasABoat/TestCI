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
    && pip3.6 install Flask \
                      gunicorn \
                      PyYAML \
                      requests \
    && yum --enablerepo=* clean all \
    && rm -rf /var/cache/yum

CMD ["python","/opt/myapp/api.py"]
COPY myapp /opt/myapp