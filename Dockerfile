FROM python:3.9.10

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "flask","run","--host","0.0.0.0" ]