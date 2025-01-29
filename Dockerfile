FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04
WORKDIR /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Python files
COPY handler.py .

# Start Ollama server and pull model at runtime
CMD ollama serve > /dev/null 2>&1 & \
    sleep 10 && \
    ollama pull deepseek-r1:1.5b && \
    python -u handler.py
