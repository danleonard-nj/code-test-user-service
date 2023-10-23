FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get dist-upgrade -y
EXPOSE 80

CMD ["bash", "startup.sh"]
