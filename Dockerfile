FROM ghcr.io/infrasonar/python:3.14.3
ADD . /code
WORKDIR /code
RUN apt-get update && \
    apt-get install -y iperf3 && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /data
CMD ["python", "main.py"]
