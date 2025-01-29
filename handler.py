import os
import time
import threading
from typing import Dict
from fastapi import FastAPI
from runpod import ServerlessHandler
import ollama  # Ollama Python client

app = FastAPI()
LAST_REQUEST_TIME = time.time()
SHUTDOWN_DELAY = 300  # 5 minutes of inactivity

def schedule_shutdown():
    """
    Starts a thread to shut down the container after inactivity.
    """
    def shutdown():
        time.sleep(SHUTDOWN_DELAY)
        if (time.time() - LAST_REQUEST_TIME) >= SHUTDOWN_DELAY:
            print("🛑 Shutting down due to inactivity...")
            os._exit(0)  # Force-terminate the container

    # Run shutdown timer in a background thread
    shutdown_thread = threading.Thread(target=shutdown, daemon=True)
    shutdown_thread.start()

@app.post("/generate")
async def generate(payload: Dict):
    global LAST_REQUEST_TIME
    LAST_REQUEST_TIME = time.time()  # Reset inactivity timer

    prompt = payload.get("prompt", "")
    
    # Generate response using Ollama
    response = ollama.generate(
        model="deepseek-r1:32b",
        prompt=prompt,
        options={"temperature": 0.7}
    )
    
    schedule_shutdown()  # Restart the shutdown timer
    return {"response": response["response"]}

# RunPod handler
handler = ServerlessHandler(app)
