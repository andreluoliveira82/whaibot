FROM python:3.13 as builder

WORKDIR /app

RUN apt-get update

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.13-slim

WORKDIR /app

# Copiar as dependências instaladas do estágio builder
COPY --from=builder /root/.local /root/.local

# Copiar o código fonte
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
