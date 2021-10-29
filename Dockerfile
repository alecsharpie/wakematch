FROM python:3.8.6-buster

ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
WORKDIR $APP_HOME

COPY wakematch /wakematch
COPY app.py /app.py
COPY requirements.txt /requirements.txt

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN groupadd -r app && useradd -r -g app app

COPY --chown=app:app . ./
USER app

CMD exec gunicorn --bind :$PORT --log-level info --workers 1 --threads 8 --timeout 0 app:server
