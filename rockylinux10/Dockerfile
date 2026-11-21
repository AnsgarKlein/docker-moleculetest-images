FROM rockylinux/rockylinux:10

LABEL maintainer="Ansgar Klein"

# Don't skip installation of documentation
RUN sed -i 's/tsflags=nodocs//' /etc/yum.conf

RUN dnf -y install rpm dnf-plugins-core \
    # Install systemd \
    && dnf -y install systemd \
    # Install python \
    && dnf -y install python \
    && dnf clean all

# We need to mount hosts `/sys/fs/cgroup` read-writeable into container for
# systemd to work.
VOLUME ["/sys/fs/cgroup"]
CMD ["/lib/systemd/systemd"]
