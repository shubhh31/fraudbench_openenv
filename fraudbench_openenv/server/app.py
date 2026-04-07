# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the Fraudbench Openenv Environment.
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    uv sync\n'"
    ) from e

from fraudbench_openenv.models import Action, Observation
from fraudbench_openenv.server.fraudbench_openenv_environment import (
    FraudBenchOpenenvEnvironment,
)

app = create_app(
    FraudBenchOpenenvEnvironment,
    Action,
    Observation,
    env_name="fraudbench_openenv",
    max_concurrent_envs=1,
)


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()