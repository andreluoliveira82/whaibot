# Build stage usando imagem Python completa
FROM python:3.13 as builder

WORKDIR /app

RUN pip install uv==0.2.8

COPY requirements.txt .

# Criar e ativar venv
RUN uv venv && \
    . /app/.venv/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt

# Runtime stage usando imagem slim
FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]