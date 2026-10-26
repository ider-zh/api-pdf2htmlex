FROM ider/pdf2htmlex

MAINTAINER ider <ider@knogen.cn>

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /root/api-pdf2htmlex

# Build from this checkout, so PR builds do not silently clone master.
COPY . .

RUN sed -i 's/security.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list && \
    sed -i 's/archive.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list && \
    apt update && \
    apt-get -qq -y install python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# The legacy converter image predates supported Python releases. Install a
# SHA256-verified, patched Mozilla CA bundle and replace pip's vendored trust
# bundle before making any pip HTTPS requests. Also replace requests' certifi
# bundle after installation. This is a compatibility hotfix, not an OS upgrade.
RUN python3 scripts/refresh_certifi_ca.py

ENV REQUESTS_CA_BUNDLE=/usr/local/share/pdf2htmlex/certifi-2026.10.19.pem \
    SSL_CERT_FILE=/usr/local/share/pdf2htmlex/certifi-2026.10.19.pem \
    PIP_CERT=/usr/local/share/pdf2htmlex/certifi-2026.10.19.pem

RUN pip3 install flask requests pillow bs4 lxml -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python3 scripts/refresh_certifi_ca.py

EXPOSE 5000
CMD ["python3", "run.py"]
