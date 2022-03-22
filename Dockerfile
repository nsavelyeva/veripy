FROM python:3.9.10-alpine3.15

COPY src /opt/veripy
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

RUN addgroup -S veripy && \
    adduser -S veripy -G veripy
USER veripy

RUN python -m pip install --prefix=/usr/local --upgrade pip && \
    pip install --prefix=/usr/local --no-cache-dir \
        nose2[coverage_plugin] coverage pylint radon bandit

ENTRYPOINT ["/entrypoint.sh"]
