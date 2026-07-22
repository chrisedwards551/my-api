import os

from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


DATABASE_URL = get_required_env(
    "DATABASE_URL"
)

SECRET_KEY = get_required_env(
    "SECRET_KEY"
)

ALGORITHM = get_required_env(
    "ALGORITHM"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    get_required_env(
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    )
)