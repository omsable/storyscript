FROM        python:3.7-alpine

RUN         mkdir /app
ADD         requirements.txt /app
RUN         pip install -r /app/requirements.txt
RUN         pip install https://github.com/storyscript/storyscript/archive/master.zip
ADD         app.py /app/app.py

ENTRYPOINT  ["python", "/app/app.py"]
