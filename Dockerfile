FROM python:3.8-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV COMMAND_PREFIX $COMMAND_PREFIX
ENV EMOJI $EMOJI
ENV TOKEN $TOKEN
ENV SUMMON_ROLE $SUMMON_ROLE

CMD [  "python", "./main.py"]