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
