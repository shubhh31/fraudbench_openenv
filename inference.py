import json
import os
import sys
import traceback

from openai import OpenAI, OpenAIError

from models import Action
from server.fraudbench_openenv_environment import FraudBenchOpenenvEnvironment

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def make_chat_completion(model_name: str, prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=64,
            temperature=0.0,
        )
        return completion.choices[0].message.content.strip()
    except OpenAIError as exc:
        message = str(exc)
        if "model" in message.lower() and "not found" in message.lower():
            if model_name != "gpt-4o-mini":
                return make_chat_completion("gpt-4o-mini", prompt)
        raise


def choose_decision() -> str:
    prompt = (
        "You are a fraud decision assistant. Reply with exactly one word: approve, deny, or escalate. "
        "Do not include any other text."
    )
    content = make_chat_completion(MODEL_NAME, prompt).lower()
    for token in ["approve", "deny", "escalate"]:
        if token in content:
            return token
    return "approve"


def main() -> int:
    print("[START]")
    reward = 0.0
    done = False
    success = False
    error_value = None

    try:
        env = FraudBenchOpenenvEnvironment()
        env.reset()

        decision = choose_decision()
        action = Action(decision=decision, reason="auto decision")
        observation = env.step(action)

        reward = float(observation.reward)
        done = bool(observation.done)
        success = True

        print("[STEP] env.step")
        print(f"reward: {reward:.2f}")
        print(f"done: {str(done).lower()}")
        print(f"success: {str(success).lower()}")
        print("error: null")
        return 0
    except Exception as exc:
        error_value = str(exc)
        tb = traceback.format_exc()
        print("[STEP] error")
        print(f"reward: {reward:.2f}")
        print(f"done: {str(done).lower()}")
        print(f"success: {str(success).lower()}")
        print(f"error: {json.dumps(error_value)}")
        print(f"traceback: {json.dumps(tb)}")
        return 1
    finally:
        print("[END]")


if __name__ == "__main__":
    sys.exit(main())
