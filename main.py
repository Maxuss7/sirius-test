from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from prometheus_client import Counter, generate_latest

app = FastAPI()

REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)
        
    REQUEST_COUNTER.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    
    return await call_next(request)

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return generate_latest()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello, stranger!</h1>"

@app.get("/{name}", response_class=HTMLResponse)
async def read_name(name: str):
    return f"<h1>Hello, {name.capitalize()}!</h1>"