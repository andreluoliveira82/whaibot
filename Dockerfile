FROM python:3.13

WORKDIR /app

COPY requirements.txt .

# Instale dependências do sistema e Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]