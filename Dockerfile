# ===== Base image used by all stages =====
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# ===== Stage 1: Builder =====
FROM base AS builder

# Build tools are needed only for compiling wheels.
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install deps into a virtualenv to keep runtime clean.
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install -r requirements.txt

# ===== Stage 2: Runtime =====
FROM base AS runtime

# Create a dedicated non-root user.
RUN adduser --disabled-password --gecos "" --home /app appuser

# Activate venv by default for all commands.
ENV PATH="/opt/venv/bin:$PATH"

# Copy virtualenv and app source.
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Fix ownership so the app can write to /app if needed.
RUN chown -R appuser:appuser /app
USER appuser

# Document the port. Set to your actual service port.
EXPOSE 8000
ENV PORT=8000

# Default start command. Replace with gunicorn/uvicorn for production.
CMD ["python", "main.py"]
