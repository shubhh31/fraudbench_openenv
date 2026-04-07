import random
import uuid
from fraudbench_openenv.models import Observation, Action, Transaction


class FraudBenchOpenenvEnvironment:
    def __init__(self):
        self.current_case = None
        self.done = False
        self.last_observation = None
        self.episode_id = ""
        self.timestep = 0

        self.case_bank = [
            {
                "case_id": "case_001",
                "transaction": {
                    "transaction_id": "tx_1001",
                    "amount": 4999.0,
                    "merchant": "QuickGiftCards",
                    "category": "digital_goods",
                    "timestamp": "2026-04-01T02:14:00Z",
                    "user_id": "u_001",
                    "device_id": "new_device_xyz",
                    "ip_address": "185.22.10.4",
                    "location": "high-risk-country",
                },
                "history_summary": "User usually spends $20-$80 on groceries locally.",
                "expected_decision": "deny",
            },
            {
                "case_id": "case_002",
                "transaction": {
                    "transaction_id": "tx_1002",
                    "amount": 42.5,
                    "merchant": "NeighborhoodMart",
                    "category": "groceries",
                    "timestamp": "2026-04-01T18:20:00Z",
                    "user_id": "u_002",
                    "device_id": "known_device_abc",
                    "ip_address": "73.44.120.8",
                    "location": "home-city",
                },
                "history_summary": "Pattern matches normal weekday grocery purchases.",
                "expected_decision": "approve",
            },
            {
                "case_id": "case_003",
                "transaction": {
                    "transaction_id": "tx_1003",
                    "amount": 1200.0,
                    "merchant": "FlyNow Airlines",
                    "category": "travel",
                    "timestamp": "2026-04-02T05:50:00Z",
                    "user_id": "u_003",
                    "device_id": "known_device_travel",
                    "ip_address": "66.31.77.9",
                    "location": "new-city",
                },
                "history_summary": "User occasionally books travel, amount slightly above average.",
                "expected_decision": "escalate",
            },
        ]

    def _obs(self, reward: float = 0.0, done: bool = False, info=None) -> Observation:
        tx = Transaction(**self.current_case["transaction"])
        return Observation(
            episode_id=self.episode_id,
            timestep=self.timestep,
            step_count=self.timestep,
            case_id=self.current_case["case_id"],
            transaction=tx,
            history_summary=self.current_case["history_summary"],
            step=1,
            max_steps=1,
            reward=reward,
            done=done,
            info=info or {},
        )

    def reset(self) -> Observation:
        self.done = False
        self.current_case = random.choice(self.case_bank)
        self.episode_id = str(uuid.uuid4())
        self.timestep = 0
        self.last_observation = self._obs(reward=0.0, done=False, info={})
        return self.last_observation

    @property
    def state(self) -> Observation:
        if self.last_observation is None:
            return self.reset()
        return self.last_observation

    def step(self, action: Action) -> Observation:
        if self.current_case is None:
            return self.reset()

        if self.done and self.last_observation is not None:
            return self.last_observation

        expected = self.current_case["expected_decision"]
        reward = 1.0 if action.decision == expected else 0.0
        self.done = True
        self.timestep += 1

        self.last_observation = self._obs(
            reward=reward,
            done=True,
            info={
                "expected_decision": expected,
                "agent_decision": action.decision,
                "match": action.decision == expected,
                "reason": action.reason,
            },
        )
        return self.last_observation

    async def reset_async(self) -> Observation:
        return self.reset()

    async def step_async(self, action: Action) -> Observation:
        return self.step(action)


FraudbenchOpenenvEnvironment = FraudBenchOpenenvEnvironment