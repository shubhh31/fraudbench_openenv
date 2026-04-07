from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models import Action
from server.fraudbench_openenv_environment import FraudBenchOpenenvEnvironment

app = FastAPI()
env = FraudBenchOpenenvEnvironment()


def to_dict(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return obj


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return JSONResponse(content=to_dict(obs))


@app.post("/step")
def step(action: Action):
    obs = env.step(action)
    return JSONResponse(content=to_dict(obs))