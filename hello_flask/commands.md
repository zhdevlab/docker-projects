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
```
