FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install celery
RUN pip install redis
COPY . /app/
EXPOSE 8000
ENV IGDB_API_URL=https://api-v3.igdb.com/
ENV IGDB_API_KEY=42f4e632a36d87e2aa2c1ef1a9ab1614
ENV TWITTER_API_KEY=XHkm8Fysq5zeuxxYHr4B6L5QD
ENV TWITTER_SECRET_API_KEY=rVFi4YSQCWKZRh67X1YzuKQg0AMokNab1QnLInWHLbztPOSX52
ENV TWITTER_API_URL=https://api.twitter.com/
ENV DB_ENGINE=django.db.backends.postgresql_psycopg2
ENV DB_NAME=django_db
ENV DB_USER=gamemuster@postgresgamemuster
ENV DB_PASSWORD=200121213Da
ENV DB_HOST=postgresgamemuster.postgres.database.azure.com
ENV DB_PORT=5432
ENV EMAIL_HOST_USER=nikitaderkovichsmtp@gmail.com
ENV EMAIL_HOST_PASSWORD=200121213DaSmtp
ENV DEBUG=''
ENV SECRET_KEY=111313123
ENV CELERY_BROKER=redis://:bnzZ1jgan39QWgeQRSAWsu+mfSXW1gw6t3X97vi1Q4o=@gamemusterazure.redis.cache.windows.net:6379/0
ENV CELERY_BACKEND=redis://:bnzZ1jgan39QWgeQRSAWsu+mfSXW1gw6t3X97vi1Q4o=@gamemusterazure.redis.cache.windows.net:6379/0
RUN python /app/manage.py collectstatic --noinput
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
