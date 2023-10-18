FROM python:3.11.6-alpine3.17

RUN mkdir /data

COPY . /data

RUN pip install -r /data/requirements.txt

WORKDIR /data

# docker run
# CMD ["gunicorn", "puyuan_case.wsgi:application", "-b", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker-compose
# 不需要CMD