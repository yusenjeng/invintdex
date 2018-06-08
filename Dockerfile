FROM python:3.6.4
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
RUN mkdir /invintdex
WORKDIR /invintdex
ADD requirements.txt /invintdex/
RUN pip3 install -r requirements.txt
ADD . /invintdex/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]