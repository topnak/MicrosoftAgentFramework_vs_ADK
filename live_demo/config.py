"""Live demo configuration — loads .env for Foundry connection."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "gpt-4o")
AGENT_NAME = os.getenv("AGENT_NAME", "supply-chain-assistant")


def is_configured() -> bool:
    """Return True if Foundry endpoint is set."""
    return bool(FOUNDRY_ENDPOINT)
