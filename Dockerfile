FROM python:3.9

WORKDIR /root

COPY ./source/ ./source/
COPY ./manage.py ./
COPY requirements.txt ./
COPY entrypoint.sh ./

ENV PYTHONPATH /root/source
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/root/entrypoint.sh"]

CMD ["gunicorn", "source.core.wsgi:application", "--bind", "0.0.0.0:8000"]
