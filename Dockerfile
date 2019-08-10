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
    pip3 install flask requests pillow bs4 lxml -i https://pypi.tuna.tsinghua.edu.cn/simple 

RUN git clone https://github.com/ider-zh/api-pdf2htmlex.git

# COPY $PWD/* api-pdf2htmlex/
EXPOSE 5000
CMD python3 api-pdf2htmlex/run.py
