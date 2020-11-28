FROM python:3.8-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV SUMMON_COMMAND $SUMMON_COMMAND
ENV EMOJI $EMOJI
ENV API_KEY $API_KEY
ENV SUMMON_ROLE $SUMMON_ROLE

CMD [  "python", "./main.py"]