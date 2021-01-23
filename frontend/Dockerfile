FROM python:3-alpine
WORKDIR /project
ADD . /project
RUN pip3 install -r requirements.txt
EXPOSE 3080
ENTRYPOINT ["python3", "app.py"]
