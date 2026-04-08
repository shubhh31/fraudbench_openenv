from openenv.core.env_server import create_app
from models import Action, Observation
from server.fraudbench_openenv_environment import FraudBenchOpenenvEnvironment


# Create the FastAPI app using OpenEnv's create_app
app = create_app(
    env=FraudBenchOpenenvEnvironment,  # Environment class (factory)
    action_cls=Action,
    observation_cls=Observation,
)


def main():
    """Entry point for running the server."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)