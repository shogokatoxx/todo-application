FROM python:3.6

RUN apt update -y && apt upgrade -y
RUN pip install pipenv

RUN mkdir /root/todo-application
WORKDIR /root/todo-application
ENV PYTHONPATH ~/.local/share/virtualenvs/todo-application-m2wz-yu3/lib/python3.6

COPY Pipfile /root/todo-application/
COPY Pipfile.lock /root/todo-application/
RUN pipenv install
