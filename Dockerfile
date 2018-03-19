FROM python:3.5.2
ENV APP_DIR /app
WORKDIR ${APP_DIR}
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
