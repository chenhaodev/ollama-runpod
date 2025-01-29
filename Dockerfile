FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04
WORKDIR /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server in the background and pre-download the model
RUN ollama serve > /dev/null 2>&1 & \
    sleep 10 && \
    ollama pull deepseek-r1:32b

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Python files
COPY handler.py .

# Start the API
CMD ["python", "-u", "handler.py"]
