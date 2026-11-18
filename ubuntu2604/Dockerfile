FROM ubuntu:26.04

LABEL maintainer="Ansgar Klein"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    # Unminimize system \
    && apt-get install -y --no-install-recommends \
       man-db \
       unminimize\
    && yes | unminimize \
    # Install systemd \
    && apt-get install -y --no-install-recommends \
       libbpf1 \
       systemd \
       systemd-sysv \
    # Install python \
    && apt-get install -y --no-install-recommends \
       python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# We need to mount hosts `/sys/fs/cgroup` read-writeable into container for
# systemd to work.
VOLUME ["/sys/fs/cgroup"]
CMD ["/lib/systemd/systemd"]
