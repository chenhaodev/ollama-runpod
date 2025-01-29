FROM runpod/base:0.12.0-cuda11.8.0
WORKDIR /app

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Python files
COPY handler.py .

# Start the API
CMD ["python", "-u", "handler.py"]
