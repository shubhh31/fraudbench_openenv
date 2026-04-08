from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import Action
from server.fraudbench_openenv_environment import FraudBenchOpenenvEnvironment

app = FastAPI()
env = FraudBenchOpenenvEnvironment()


def _to_dict(obj):
    """Recursively convert Pydantic models to dicts"""
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_dict(item) for item in obj]
    if hasattr(obj, "model_dump"):
        return _to_dict(obj.model_dump())
    if hasattr(obj, "dict"):
        return _to_dict(obj.dict())
    return obj

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return JSONResponse(content=_to_dict(obs))


@app.post("/step")
def step(action: Action):
    obs = env.step(action)
    return JSONResponse(content=_to_dict(obs))