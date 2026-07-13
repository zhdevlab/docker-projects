# Commands Used — Containerising a Flask App

## 1. Set up a virtual environment
Needed since Ubuntu blocks system-wide pip installs (externally managed
environment protection).

```bash
sudo apt update
sudo apt install python3.14-venv
python3 -m venv venv
source venv/bin/activate
```

## 2. Install Flask inside the venv
```bash
pip3 install flask
```

## 3. Run the app locally to confirm it works
```bash
python3 app.py
```
Confirms the app serves correctly before containerising it.

## 4. Write the Dockerfile
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 5002
CMD ["python", "app.py"]
```
Note: the base image is `python`, not `python3` — Docker Hub only publishes
`python`, versioned by tag (e.g. `3.8-slim`).

## 5. Build the image
```bash
docker build -t hello-flask .
```

## 6. Run the container
```bash
docker run -d -p 5002:5002 hello-flask
```
`-p <host_port>:<container_port>` maps a port on the host machine to the
port Flask listens on inside the container.

## 7. Verify it's running
```bash
docker ps
```

## 8. Stop the container
```bash
docker stop <container_id>
``








### Phase 2 — Adding MySQL

### 9. Create a custom Docker network

Needed so the Flask container and the MySQL container can reach each
other by name.

```bash
docker network create my-custom-network
```

### 10. Run a MySQL container on that network

```bash
docker run -d --name mydb --network my-custom-network -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:5.7
```

### 11. Update the Dockerfile

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config
RUN pip install flask mysqlclient
EXPOSE 5002
CMD ["python", "app.py"]
```

### 12. Rebuild the image

```bash
docker build -t hello-flask-mysql .
```

### 13. Run the Flask app on the same network as MySQL

```bash
docker run -d --name myapp --network my-custom-network -p 5002:5002 hello-flask-mysql
```

### 14. Verify both containers are running

```bash
docker ps
```

Visited `http://127.0.0.1:5002` in browser — confirmed Flask successfully
queried MySQL and returned the version string.

## Container lifecycle reference

```bash
docker stop <container>    # halts the container, keeps it on disk
docker start <container>   # resumes a stopped container
docker rm <container>      # deletes the container entirely
docker ps -a                # shows all containers, including stopped ones
````
