FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron
RUN apt-get update && apt-get install -y curl

COPY ../../crontab.txt /root/
RUN crontab /root/crontab.txt
RUN touch /var/log/cron.log

CMD /usr/sbin/cron -f
