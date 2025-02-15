ARG PYTHON_BASE=3.11-slim

# Build stage
FROM python:$PYTHON_BASE AS builder

# Install PDM
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

WORKDIR /app

# Install dependencies inside .venv
COPY pyproject.toml pdm.lock README.md ./
RUN pdm venv create --with-pip
RUN pdm install --check --prod --no-editable

COPY . .

# Run stage
FROM python:$PYTHON_BASE

# Copy installed dependencies
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . /app
WORKDIR /app

EXPOSE 7000
# CMD ["uvicorn", "carnival.app:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", "main.py"]
