FROM python:3.9.6-alpine

RUN mkdir -p /home/covid19

RUN addgroup -S covid19 && adduser -S covid19 -G covid19

ENV HOME=/home/covid19
ENV APP_HOME=/home/covid19/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN python -m venv venv
RUN source ./venv/bin/activate
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN chown -R covid19:covid19 $APP_HOME

USER covid19

ENTRYPOINT ["/home/covid19/web/entrypoint.sh"]