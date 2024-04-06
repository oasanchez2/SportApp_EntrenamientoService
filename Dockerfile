FROM python:3.10-slim

COPY . ./app

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "application.py"]