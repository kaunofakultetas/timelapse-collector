FROM python:3.13.1-alpine

WORKDIR /app

RUN pip install requests pytz

COPY main.py /app/main.py

CMD ["python3", "-u", "main.py"]