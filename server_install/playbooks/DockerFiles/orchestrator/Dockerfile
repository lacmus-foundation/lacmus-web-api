FROM python:3.7
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
WORKDIR /app/orchestrator
CMD python main.py