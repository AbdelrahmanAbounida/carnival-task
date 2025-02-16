.PHONY: start stop clean check-deps build run

ENV?=local
RUNNER?=python # docker , python

# Docker, pdm, and Python commands
DOCKER_IMAGE = carnival
PDM_COMMAND = pdm
PYTHON_COMMAND = python

# Default target
help:
	@echo "Usage: make [target] ENV=[local|prod] RUNNER=[pdm|docker|python]"
	@echo "  start       Start the server"
	@echo "  stop        Stop the server"
	@echo "  clean       Remove build artifacts"
	@echo "  check-deps  Check for required dependencies"

# Check if .env file exists, if not, create it from .env.example
check-env:
	@if [ ! -f .env ]; then \
		echo ".env file not found. Creating from .env.example..."; \
		cp .env.example .env; \
	else \
		echo ".env file exists."; \
	fi

# Check for required dependencies (Docker, PDM, or Python)
check-deps: check-env
	@echo "Checking dependencies..."
	@if [ "$(RUNNER)" = "docker" ] && ! command -v docker &> /dev/null; then \
		echo "Error: Docker is not installed."; exit 1; \
	elif [ "$(RUNNER)" = "pdm" ] && ! command -v $(PDM_COMMAND) &> /dev/null; then \
		echo "Error: pdm is not installed. Run 'pip install pdm'"; exit 1; \
	elif [ "$(RUNNER)" = "python" ] && ! command -v $(PYTHON_COMMAND) &> /dev/null; then \
		echo "Error: Python is not installed."; exit 1; \
	elif [ "$(RUNNER)" = "python" ] && [ ! -f requirements.txt ]; then \
		echo "Error: requirements.txt file not found."; exit 1; \
	fi
	@echo "All dependencies are installed."

build: check-deps
	@echo "Building the project..."
	@echo "RUNNER is set to $(RUNNER)"  # Log the value of RUNNER
	@if [ "$(RUNNER)" = "docker" ]; then \
		docker build -t $(DOCKER_IMAGE) .; \
	elif [ "$(RUNNER)" = "pdm" ]; then \
		$(PDM_COMMAND) install; \
	elif [ "$(RUNNER)" = "python" ]; then \
		$(PYTHON_COMMAND) -m pip install -r requirements.txt; \
	else \
		echo "Error: Invalid runner. Please set RUNNER to 'docker', 'pdm', or 'python'"; exit 1; \
	fi


# Start the application using Docker, PDM, or Python
start: build
	@echo "Starting the application..."
	@if [ "$(RUNNER)" = "docker" ]; then \
		docker run -it -p 7000:7000 $(DOCKER_IMAGE); \
	elif [ "$(RUNNER)" = "pdm" ]; then \
		$(PDM_COMMAND) run main.py; \
	elif [ "$(RUNNER)" = "python" ]; then \
		$(PYTHON_COMMAND) main.py; \
	else \
		echo "Error: Invalid runner. Please set RUNNER to 'docker', 'pdm', or 'python'"; exit 1; \
	fi

# Stop the application (only for Docker)
stop:
	@echo "Stopping the application..."
	@if [ "$(RUNNER)" = "docker" ]; then \
		docker stop $(shell docker ps -q --filter ancestor=$(DOCKER_IMAGE)); \
	elif [ "$(RUNNER)" = "docker-compose" ]; then \
		docker-compose down; \
	else \
		echo "Stop is only applicable in Docker or Docker Compose mode"; exit 1; \
	fi

# Clean build artifacts (Docker, PDM, or Python)
clean:
	@echo "Cleaning up..."
	@if [ "$(RUNNER)" = "docker" ]; then \
		docker rmi $(DOCKER_IMAGE); \
	elif [ "$(RUNNER)" = "pdm" ]; then \
		$(PDM_COMMAND) run clean; \
	elif [ "$(RUNNER)" = "python" ]; then \
		$(PYTHON_COMMAND) -m pip uninstall -r requirements.txt; \
	else \
		echo "Error: Invalid runner. Please set RUNNER to 'docker', 'pdm', or 'python'"; exit 1; \
	fi
run: build start
