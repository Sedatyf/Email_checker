FROM python:3

RUN pip3 install python-dotenv
RUN pip3 install requests
WORKDIR /home/app/Email_checker
COPY . .
ENTRYPOINT ["python3", "app/main.py"]