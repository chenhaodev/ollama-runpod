import os
import time
import subprocess
from typing import Dict
from fastapi import FastAPI
from runpod import ServerlessHandler

app = FastAPI()
LAST_REQUEST_TIME = time.time()
SHUTDOWN_DELAY = 300  # 5 minutes of inactivity

# Load model at cold start
def load_model():
    subprocess.run(["ollama", "pull", "deepseek-r1:32b"], check=True)

load_model()

# Auto-shutdown logic
def schedule_shutdown():
    def shutdown():
        time.sleep(SHUTDOWN_DELAY)
        if (time.time() - LAST_REQUEST_TIME) >= SHUTDOWN_DELAY:
            print("Shutting down...")
            os._exit(0)
    
    import threading
    threading.Thread(target=shutdown, daemon=True).start()

# API endpoint
@app.post("/generate")
async def generate(payload: Dict):
    global LAST_REQUEST_TIME
    LAST_REQUEST_TIME = time.time()
    
    prompt = payload.get("prompt", "")
    response = ollama.generate(
        model="deepseek-r1:32b",
        prompt=prompt,
        options={"temperature": 0.7}
    )
    
    schedule_shutdown()
    return {"response": response}

# RunPod handler
handler = ServerlessHandler(app)
