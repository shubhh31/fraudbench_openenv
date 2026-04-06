from typing import Any, Dict, Literal
from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    merchant: str
    category: str
    timestamp: str
    user_id: str
    device_id: str
    ip_address: str
    location: str


class Action(BaseModel):
    decision: Literal["approve", "deny", "escalate"]
    reason: str = ""


class Observation(BaseModel):
    # OpenEnv runtime-required metadata
    episode_id: str = ""
    timestep: int = 0
    step_count: int = 0

    # Task payload
    case_id: str
    transaction: Transaction
    history_summary: str
    step: int = 1
    max_steps: int = 1

    # OpenEnv runtime-required
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = Field(default_factory=dict)