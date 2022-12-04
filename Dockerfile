# syntax=docker/dockerfile:1

FROM python:3.10.7 as builder

# For more info about datadog visit: https://docs.datadoghq.com/agent/basic_agent_usage/heroku/#using-heroku-with-docker-images

# Set arg
ARG database_url
ARG database_name

# Set env
ENV DB_NAME=${database_name}
ENV MONGODB_URL=${database_url}
ENV DD_DYNO_HOST=false
ENV DD_APM_ENABLED=true
ENV DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true

RUN mkdir /app
WORKDIR /app
COPY . /app
COPY datadog-config/ /etc/datadog-agent/

# Install GPG dependencies
RUN apt-get update \
 && apt-get install -y gnupg apt-transport-https gpg-agent curl ca-certificates

# Add Datadog repository and signing keys
ENV DATADOG_APT_KEYRING="/usr/share/keyrings/datadog-archive-keyring.gpg"
ENV DATADOG_APT_KEYS_URL="https://keys.datadoghq.com"
RUN sh -c "echo 'deb [signed-by=${DATADOG_APT_KEYRING}] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
RUN touch ${DATADOG_APT_KEYRING}
RUN curl -o /tmp/DATADOG_APT_KEY_CURRENT.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_CURRENT.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_CURRENT.public
RUN curl -o /tmp/DATADOG_APT_KEY_F14F620E.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_F14F620E.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_F14F620E.public
RUN curl -o /tmp/DATADOG_APT_KEY_382E94DE.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_382E94DE.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_382E94DE.public

# Expose DogStatsD and trace-agent ports
EXPOSE 8125/udp 8126/tcp

# Install the Datadog Agent
RUN apt-get update && apt-get -y --force-yes install --reinstall datadog-agent

# Build dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash", "./scripts/entrypoint.sh"]
