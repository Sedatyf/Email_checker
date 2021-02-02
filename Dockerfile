FROM python:latest

RUN pip3 install python-dotenv
RUN pip3 install requests
RUN pip3 install imapclient
RUN pip3 install pyzmail36
WORKDIR /home/app/Email_checker
COPY . .
ENTRYPOINT ["python3", "app/main.py"]