FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/identity_api
CMD uvicorn server:app --host 0.0.0.0 --port 5002
EXPOSE 5002