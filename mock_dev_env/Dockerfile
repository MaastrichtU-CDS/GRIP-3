FROM ghcr.io/coder/code-server:bookworm

# add argument with version of vantage6
ARG VANTAGE6_VERSION=4.9.1

RUN sudo apt update && sudo apt upgrade -y

RUN sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python-is-python3 \
    build-essential

RUN pip install --break-system-packages vantage6=={VANTAGE6_VERSION} vantage6-algorithm-tools=={VANTAGE6_VERSION}

# docker build -t coder_env --no-cache .
# docker run --rm --name coder -p 8080:8080 -e PASSWORD=12345 coder_env