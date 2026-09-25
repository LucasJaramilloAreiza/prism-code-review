import asyncio
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db, save_report, get_history
from backend.models import ReviewRequest
from backend.agents.orchestrator import Orchestrator

review_queues: dict[str, asyncio.Queue] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="PRism", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/review")
async def create_review(req: ReviewRequest):
    review_id = str(uuid.uuid4())
    queue: asyncio.Queue = asyncio.Queue()
    review_queues[review_id] = queue

    async def run():
        orch = Orchestrator()
        report = await orch.run(req.pr_url, req.mode, queue, review_id=review_id)
        try:
            await save_report(report)
        except Exception:
            pass
        # Keep queue alive 30s so late WS connections can still receive review_complete
        await asyncio.sleep(30)
        review_queues.pop(review_id, None)

    asyncio.create_task(run())
    return {"id": review_id}

@app.get("/api/history")
async def history(limit: int = 20, offset: int = 0):
    return await get_history(limit=limit, offset=offset)

@app.websocket("/ws/review/{review_id}")
async def ws_review(websocket: WebSocket, review_id: str):
    await websocket.accept()
    queue = review_queues.get(review_id)
    if not queue:
        await websocket.send_json({"event": "error", "message": "Review not found or already expired"})
        await websocket.close()
        return
    try:
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=120)
            except asyncio.TimeoutError:
                await websocket.send_json({"event": "error", "message": "Review timed out"})
                break
            await websocket.send_json(event)
            if event.get("event") in ("review_complete", "error"):
                break
    except WebSocketDisconnect:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
