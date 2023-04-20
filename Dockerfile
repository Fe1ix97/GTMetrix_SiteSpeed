FROM joyzoursky/python-chromedriver:3.8-alpine

# Timezone Settings
RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Europe/Rome /etc/localtime

COPY . .
ENV TZ=Europe/Rome
RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install -r requirements.txt


RUN cat /crontab | crontab -
CMD ["crond","-f"]