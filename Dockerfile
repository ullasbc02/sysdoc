FROM ubuntu:22.04

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    procps \
    curl \
    grep \
    findutils \
    coreutils \
    vim \
    net-tools \
    iproute2 \
    lsof \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]