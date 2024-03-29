FROM python:3.10.8-alpine3.15

COPY src /opt/veripy
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# can be required for project dependencies such as numpy
RUN apk add gcc g++

RUN python -m pip install --prefix=/usr/local --no-cache-dir --upgrade pip \
    && pip install --prefix=/usr/local --no-cache-dir \
        nose2[coverage_plugin] coverage pylint radon bandit

ENTRYPOINT ["/entrypoint.sh"]
