FROM       ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["run.py"]
