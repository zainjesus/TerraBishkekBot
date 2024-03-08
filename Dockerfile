FROM python:3.10

EXPOSE 7315

RUN mkdir -p /opt/services/bot
WORKDIR /opt/services/bot/

COPY . /opt/services/bot/

RUN pip install -r requirements.txt

CMD ["python", "/opt/services/bot/main.py"]