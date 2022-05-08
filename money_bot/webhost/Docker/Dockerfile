# Python
FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
     && pip install setuptools \
     && pip install --no-cache-dir -r requirements.txt


# Tools
COPY . /code/

# Gunicorn
RUN pip install gunicorn[gevent]

# Ports
EXPOSE 80
EXPOSE 2222

# Entrypoint
COPY Docker/entrypoint.sh /usr/local/bin
RUN chmod u+x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]