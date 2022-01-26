FROM python:3.9.10-alpine3.15

RUN pip install --no-cache-dir \
        pytest nose2[coverage_plugin] mock \
        coverage pylint radon bandit

COPY src /opt/veripy
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
