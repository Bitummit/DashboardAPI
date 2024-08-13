FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR code

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
