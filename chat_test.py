from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Chat API Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "quantum_education"

class ChatResponse(BaseModel):
    response: str
    context: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if "superposition" in request.message.lower():
        response = "Superposition is a fundamental quantum principle where a qubit can exist in multiple states simultaneously. For example, a qubit can be in both |0⟩ and |1⟩ states at once, written as α|0⟩ + β|1⟩ where α and β are probability amplitudes."
    elif "bloch" in request.message.lower():
        response = "The Bloch sphere is a geometric representation of qubit states. Every point on the sphere represents a possible quantum state."
    else:
        response = "I'm here to help you learn quantum computing! Ask me about quantum gates, algorithms, superposition, entanglement, or how to use this platform."
    
    return ChatResponse(response=response, context=request.context)

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)