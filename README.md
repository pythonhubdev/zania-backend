# Zania Backend

A FastAPI-based Question-Answering API leveraging Langchain and large language models. Answers questions based on
uploaded JSON or PDF documents, providing a structured JSON output of question-answer pairs.

# Installing UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

# Installing packages with uv

```bash
uv sync
```

# Setting up `.env`
Add the following to your `.env.development` file:

```dotenv
DEBUG=True
SECRET_KEY=<your_secret_key>
NAME="Zania Backend"
APP_LOC=zania_backend.web.application:app
HOST=0.0.0.0
PORT=8000
WEB_CONCURRENCY=1
USE_HYPERCORN=True
ENVIRONMENT=development
OPENAI_API_KEY=<your_openai_api_key>
LOG_LEVEL=20
```

# Running the server

```bash
uv run python -m src
```


# View the Docs in two formats

1. http://0.0.0.0:8000/api/docs - Swagger
2. http://0.0.0.0:8000/api/scalar - Scalar
