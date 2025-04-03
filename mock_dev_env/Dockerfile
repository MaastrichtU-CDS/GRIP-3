FROM ghcr.io/coder/code-server:bookworm

RUN sudo apt update && sudo apt upgrade -y

RUN sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential

RUN pip install --break-system-packages vantage6 vantage6-algorithm-tools

# docker build -t coder_env --no-cache .
# docker run --rm --name coder -p 8080:8080 -e PASSWORD=12345 coder_env