FROM python:3.12-slim
LABEL authors="Dmitry Z."

WORKDIR /src

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY src .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]