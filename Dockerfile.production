FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN git clone https://github.com/jesusenlanet/django-example.git /code
WORKDIR /code
RUN pip install --upgrade pip && pip install -r requirements.txt
