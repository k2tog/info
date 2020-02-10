FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ARG VERSION="0.0.0"
ENV VERSION=${VERSION}
ARG SERVICE_NAME="BLANK"
ENV SERVICE_NAME=${SERVICE_NAME}
ARG COMMIT_SHA="1290a2f"
ENV GIT_COMMIT_SHA=${COMMIT_SHA}

EXPOSE 5000/tcp

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]