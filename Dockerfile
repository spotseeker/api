FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/ ./requirements

RUN pip install --no-cache-dir -r requirements/local.txt

COPY . .

EXPOSE 8000
ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]
