import os
import sys
from typing import Optional

from openai import OpenAI, OpenAIError

DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL_NAME = "gpt-4o-mini"


def get_env_vars() -> tuple[str, str, str]:
    api_base_url = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
    model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise EnvironmentError(
            "HF_TOKEN environment variable is required and must be set."
        )
    return api_base_url, model_name, hf_token


def create_openai_client(api_base_url: str, hf_token: str) -> OpenAI:
    return OpenAI(api_key=hf_token, base_url=api_base_url)


def validate_token(client: OpenAI) -> None:
    try:
        client.models.list()
    except OpenAIError as exc:
        raise RuntimeError(
            "HF_TOKEN validation failed. Please verify HF_TOKEN is set and valid."
        ) from exc


def generate_response(client: OpenAI, model_name: str, prompt: str) -> str:
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
    )

    message = completion.choices[0].message
    if message is None:
        return ""
    return message.content


def run_demo(prompt: Optional[str] = None) -> int:
    api_base_url, model_name, hf_token = get_env_vars()
    client = create_openai_client(api_base_url, hf_token)
    validate_token(client)

    prompt = prompt or "Hello from OpenEnv demo. Please reply with a short confirmation."
    output = generate_response(client, model_name, prompt)

    print("[START]")
    print("[STEP] prompt_sent")
    print(output)
    print("[END]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run_demo())
    except Exception as exc:
        print("[START]")
        print("[STEP] error")
        print(str(exc))
        print("[END]")
        sys.exit(1)
