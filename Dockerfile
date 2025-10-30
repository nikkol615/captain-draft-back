FROM python:3.12
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY pyproject.toml poetry.lock main.py ./
COPY database ./database
COPY models ./models
COPY config ./config
COPY api ./api
RUN poetry install -n

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "teasy.main:app", "--host", "0.0.0.0", "--port", "3000"]