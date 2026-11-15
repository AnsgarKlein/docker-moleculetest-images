FROM ubuntu:26.04

LABEL maintainer="Ansgar Klein"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    # Unminimize system \
    && apt-get install -y --no-install-recommends \
       man-db \
       unminimize\
    && yes | unminimize \
    # Install python \
    && apt-get install -y --no-install-recommends \
       libbpf1 \
       systemd \
       systemd-sysv \
    # Install python \
    && apt-get install -y --no-install-recommends \
       python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

VOLUME ["/sys/fs/cgroup", "/run"]
CMD ["/lib/systemd/systemd"]
