   FROM python:3.12-slim

   RUN pip install uv

   WORKDIR /app

   COPY pyproject.toml uv.lock README.md ./
   RUN uv sync --frozen --no-dev --no-install-project

   COPY src ./src
   COPY docs ./docs
   COPY ui ./ui
   RUN uv sync --frozen --no-dev

   ENV PATH="/app/.venv/bin:$PATH"

   EXPOSE 8000
   CMD ["uvicorn", "emg_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]