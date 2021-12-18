FROM python:3.8.5
WORKDIR /app
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
COPY /backend .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
