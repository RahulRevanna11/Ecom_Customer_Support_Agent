from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load the model into memory once when the server starts
print("Loading GPT-2 Small model...")
generator = pipeline("text-generation", model="" \
"gpt2-medium")
print("Model loaded successfully!")

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 50

@app.post("/generate")
def generate_text(request: PromptRequest):
    # Run inference on the model
    # Example formatting inside app.py
    formatted_prompt = f"System: You are a customer support assistant.\nUser: {request.prompt}\nAssistant:"

    results = generator(formatted_prompt, max_length=request.max_length, num_return_sequences=10)
    return {"generated_text": results[0]["generated_text"]}
