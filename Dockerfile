FROM python:3.8-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY . .

CMD ["uvicorn", "botnet-api:app", "--host", "0.0.0.0", "--port", "8100"]
