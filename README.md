# Molecule Test Containers

[![Build container images](https://github.com/AnsgarKlein/docker-moleculetest-images/actions/workflows/build.yml/badge.svg)](https://github.com/AnsgarKlein/docker-moleculetest-images/actions/workflows/build.yml)

Minimal Linux containers for testing Ansible roles and playbooks with
[Molecule](https://ansible.readthedocs.io/projects/molecule/). Each image
aims to mimic a valid minimal OS installation (including `systemd`!).

To make it possible for Ansible to connect to the "host" Python will be
installed from the systems repositories (and thus might be quite old).

## Automatically built images

A GitHub Actions workflow builds each image regularly and pushes it to Docker Hub.

Published images are available on Docker Hub as
`ansgarklein/moleculetest-<image-directory>:latest`.

## Build images locally

Install Docker with Buildx and
Python 3. The build script uses only the Python standard library.

From the repository root, build all images:

```sh
python3 build.py
```

Build one or more images by directory name:

```sh
python3 build.py ubuntu2604
python3 build.py ubuntu2604 rockylinux9
python3 build.py rockylinux*
```

## Run a container

For example, pull and start an Ubuntu 24.04 container:

```sh
docker run --detach \
  --name molecule-test \
  --privileged \
  --volume=/sys/fs/cgroup:/sys/fs/cgroup:rw \
  --cgroupns=host \
  ansgarklein/moleculetest-ubuntu2404:latest
```

The container runs `systemd` as its default command. The privileged mode and
cgroup mount are needed for systemd-based testing.
Stop and remove the example container when finished:

```sh
docker stop molecule-test
docker rm molecule-test
```

## License

This project's original files are licensed under the [MIT License](LICENSE).
Base images and software included in the resulting container images are
of course subject to their respective licenses.
