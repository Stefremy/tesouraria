# Multi-stage Dockerfile for Tesouraria application
# This Dockerfile supports both Python and Node.js applications

# Stage 1: Build stage (for applications that need compilation)
FROM python:3.11-slim as builder

WORKDIR /app

# Copy dependency files
COPY requirements*.txt package*.json ./

# Install Python dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir --user -r requirements.txt; \
    fi

# Install Node.js dependencies if package.json exists
RUN if [ -f package.json ]; then \
    apt-get update && apt-get install -y nodejs npm && \
    npm ci --only=production; \
    fi

# Stage 2: Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install Node.js runtime if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Make sure scripts are executable
RUN if [ -f deploy.sh ]; then chmod +x deploy.sh; fi
RUN if [ -f start.sh ]; then chmod +x start.sh; fi

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health').read()" || exit 1

# Default command - can be overridden
CMD if [ -f start.sh ]; then ./start.sh; elif [ -f main.py ]; then python main.py; elif [ -f app.py ]; then python app.py; elif [ -f server.js ]; then node server.js; elif [ -f index.js ]; then node index.js; else echo "No entry point found. Please specify CMD in docker run or add start.sh"; exit 1; fi
