FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

COPY . .

EXPOSE 8000

CMD ["wait-for-it", "db:5432", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
