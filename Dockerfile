FROM python:3

RUN pip3 install python-dotenv
WORKDIR /home/app/Email_checker
COPY . .
ENTRYPOINT ["python3", "main.py"]