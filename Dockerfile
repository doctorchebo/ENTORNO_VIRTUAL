FROM python:3.10

RUN apt update && \
    apt install -y nano netcat-traditional

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/wait-for-it.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CRUD.wsgi:application"]