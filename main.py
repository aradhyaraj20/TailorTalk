from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import graph  # assuming you have LangGraph setup in agent.py
import traceback

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or explicitly use ["http://localhost:8000"] for Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data["message"]

        # Run the LangGraph agent
        response = graph.invoke({"history": [{"type": "human", "content": user_input}]})
        
        return {"response": response["history"][-1]["content"]}
    
    except Exception as e:
        traceback.print_exc()
        return {
            "response": f"❌ Server Error: {str(e)}"
        }
