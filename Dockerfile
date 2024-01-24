FROM python:3.12 as requirements
RUN python3.12 -m pip install --no-cache-dir --upgrade poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.12-slim as final

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY --from=requirements /requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
