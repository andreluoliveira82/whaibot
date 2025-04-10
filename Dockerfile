FROM python:3.13

WORKDIR /app

COPY requirements.txt .

# install uv 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

# create virtual environment
RUN uv venv

# Install dependencies from requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    uv pip install --no-cache-dir -r requirements.txt
    #pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]