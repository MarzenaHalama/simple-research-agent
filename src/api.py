import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from src.agent import run_agent, run_agent_stream
from src.models import ResearchRequest, ResearchResponse, ErrorResponse

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="Simple Research Agent",
    description="AI research agent with Google Search grounding",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

"""
API Endpoints:
- GET /health: Health check endpoint.   
- POST /research: Accepts a research prompt, runs the agent, and returns the final response once completed.
- POST /research/stream: Accepts a research prompt and returns a stream of updates after
each iteration, allowing clients to see the agent's progress in real time.

The API uses FastAPI for handling HTTP requests and responses. 
The /research endpoint provides a blocking response with the final result, while the /research/stream endpoint uses Server-Sent Events       
(SSE) to stream updates back to the client after each iteration of the agent's loop. 

"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/research", response_model=ResearchResponse, responses={500: {"model": ErrorResponse}})
def research(request: ResearchRequest):
    result = run_agent(request.prompt)
    return result


@app.post("/research/stream")
def research_stream(request: ResearchRequest):

    def event_generator():
        for update in run_agent_stream(request.prompt):
            data = json.dumps(update.model_dump(), ensure_ascii=False)
            yield f"data: {data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
