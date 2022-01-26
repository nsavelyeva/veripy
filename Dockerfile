FROM python:3.9.10-alpine3.15

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
        nose2[coverage_plugin] coverage pylint radon bandit

COPY src /opt/veripy
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
