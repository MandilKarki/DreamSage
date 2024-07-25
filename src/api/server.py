from fastapi import FastAPI
from langserve import add_routes
from src.rag.dream_interpreter import DreamInterpreter

app = FastAPI(
    title="Dream Interpreter API",
    version="1.0",
    description="An API for interpreting dreams",
)

# Initialize the DreamInterpreter
interpreter = DreamInterpreter()

# Add routes for the dream interpretation chain
add_routes(
    app,
    interpreter.get_qa_chain(),
    path="/dream-interpretation",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)