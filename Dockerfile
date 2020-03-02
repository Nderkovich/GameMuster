FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
ARG DJANGO_SETTINGS_MODULE=GameMuster.defaultsettings
RUN ["python", "/app/manage.py", "collectstatic", "--noinput"]
ARG DJANGO_SETTINGS_MODULE=GameMuster.settings
EXPOSE 8000
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
