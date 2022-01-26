FROM python:3.9.10-alpine3.15

RUN pip install --no-cache-dir \
        nose mock unittest-xml-reporting html-testRunner \
        coverage pylint radon bandit \
    && mkdir -p /tmp/results/reports

COPY src /opt/veripy
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
