# Notes — Containerising a Flask App

## Purpose

Small Flask app, containerised to see containerisation work in practice.
Not about the app itself, the point was the build, the isolation, and the
run.

## Challenges

**Flask install blocked locally**

Tried `pip3 install flask` and got hit with Python's externally managed
environment protection. Ubuntu locks down system-wide pip installs so a
stray package doesn't break something the OS depends on.

Fix: created a venv, isolated the project's dependencies, installed Flask
inside it. No sudo, no override flags needed.

**Wrong base image in the Dockerfile**

Referenced `python3` as the base image. Docker Hub only publishes `python`,
versioned by tag. Build failed immediately, before a single layer resolved.

Fix: changed `FROM python3:3.8-slim` to `FROM python:3.8-slim`.

## What I learnt

- Same isolation principle at two different scales: a venv isolates Python
  packages, a container isolates the whole runtime.
- A wrong base image reference fails the build straight away, same as a
  broken dependency pin. Neither gets far enough to expose anything else
  that might be wrong.
- `-p host_port:container_port` maps a port on the host to the port the
  app is actually listening on inside the container. Numbers don't have to
  match.


## Phase 2 — Adding MySQL

### Purpose
Extended the single-container setup into two containers — Flask and MySQL
— to get container-to-container communication working, not just a single
isolated container running on its own.

### Challenges

**`mysqlclient` failed to compile**

- error codes:
 /bin/sh: 1: pkg-config: not found
Exception: Can not find valid pkg-config name.



`mysqlclient` isn't pure Python — it compiles a C extension against
MySQL/MariaDB headers, and the slim base image doesn't ship build tools
by default.

* Fix: installed `gcc`, `python3-dev`, `libmariadb-dev`, and `pkg-config` in the Dockerfile before `pip install`.

**Directory mix-up on rebuild**

Ran `docker build` from `~/docker` instead of `~/docker/hello_flask`
after stepping away. Docker couldn't find the Dockerfile. Reminder to
confirm the working directory before running build commands.

### What I learnt
- Containers are isolated by default — two containers can't talk to each
  other unless explicitly placed on the same Docker network.
- On a shared network, containers resolve each other by **container
  name** instead of IP address (`host="mydb"` in the Flask app connects
  straight to the MySQL container).
- A missing system-level build dependency fails a `pip install` the same
  way a wrong base image fails a build — both stop the process before
  revealing anything else.
- `docker stop` halts a container but keeps it on disk; `docker rm` is
  what actually deletes it.
