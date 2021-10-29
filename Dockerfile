FROM python:3.8.6-buster

COPY wakematch /wakematch
COPY app.py /app.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
