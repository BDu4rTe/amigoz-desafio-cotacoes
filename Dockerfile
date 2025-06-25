FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

ENV QUOTATION_SERVICE_HOST=http://localhost  
ENV QUOTATION_SERVICE_PORT=3000

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root --without=dev

COPY amigoz_desafio_cotacoes ./amigoz_desafio_cotacoes

CMD ["poetry", "run", "uvicorn", "amigoz_desafio_cotacoes.main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080