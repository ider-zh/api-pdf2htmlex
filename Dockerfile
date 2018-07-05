FROM ider/pdf2htmlex

MAINTAINER ider <ider@knogen.cn>

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /root

RUN sed -i 's/security.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list && \
    sed -i 's/archive.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list && \
    apt update && \
    apt-get -qq -y install git python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install flask requests && \
    git clone https://gitee.com/ider001/api-pdf2htmlex.git && \
    cd api-pdf2htmlex && \

RUN python3 run.py
