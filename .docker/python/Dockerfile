FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update && apt-get install -y cron && \
    apt-get update && apt-get install -y curl

WORKDIR /app

COPY ./requirements.txt /app
COPY ../../crontab.txt /etc/cron.d/crontab.txt

# Cron
RUN chmod 0644 /etc/cron.d/crontab.txt
RUN crontab /etc/cron.d/crontab.txt
RUN touch /var/log/cron.log

RUN pip install -r /app/requirements.txt

COPY . /app

CMD cron && sh ../start.sh
