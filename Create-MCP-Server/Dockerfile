FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install uv
RUN uv sync --frozen

# Copy application code
COPY main.py ./
COPY papers/ ./papers/

# Create papers directory if it doesn't exist
RUN mkdir -p papers

# Expose port (if needed for future web interface)
EXPOSE 8000

# Set the default command
CMD ["python", "main.py"]
