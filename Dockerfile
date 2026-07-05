FROM python:3.11-slim-bookworm


# System dependencies required by aeneas
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    espeak \
    libespeak-dev \
    ffmpeg \
    libsndfile1 \
    git \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Prevent pip from pulling modern incompatible build chain
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install aeneas (force legacy build mode)
RUN pip install --no-cache-dir --no-build-isolation aeneas
