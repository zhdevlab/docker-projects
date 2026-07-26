# Notes — Multi-Container Flask + Redis Challenge

## Purpose
A CoderCo challenge to build a multi-container app: Flask using Redis as a
key-value store to track a visit counter, containerised and orchestrated
with Docker Compose. Bonus objectives extended it into persistence,
externalised configuration, and horizontal scaling with load balancing.

## Challenges

**Understanding volumes**
Wasn't clear at first why Redis needed a volume, or why the mount path
had to be a specific folder. Redis's own image declares `/data` as where
it writes persistent data (`VOLUME /data`, documented on Docker Hub) —
the volume has to be mounted at that exact path to actually intercept
what Redis writes, not an arbitrary location.

**Hardcoded config vs environment variables**
Initially had `host='redis'` and `port=6379` hardcoded directly in
`app.py`. Reworked to read both from environment variables via
`os.environ.get()`, with the actual values set in `docker-compose.yml`.
Means the code doesn't need to change (or be rebuilt) if the Redis
location ever changes.

**`build:` vs `image:` — again**
Repeated the same mistake as the hello_flask project: pointing `build:`
at an image tag instead of a path. Reinforced why actively-developed
services need `build: .` (rebuilds from the current Dockerfile), while
unchanging services like Redis just reference `image:`.

**Scaling and the port conflict**
Scaling `web` to multiple replicas meant they couldn't all bind the same
host port. Switched from `ports: "5000:5000"` to `expose: "5000"` on the
`web` service, so it's reachable only within the Docker network. Only
Nginx (the single entry point) binds a host port.


