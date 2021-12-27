FROM python:3.9-alpine

COPY . .

RUN pip3 install tox
RUN tox -e py39 python manage.py makemigrations
RUN tox -e py39 python manage.py migrate

EXPOSE 8000
CMD ["tox", "-e", "py39", "python", "manage.py", "runserver", "0.0.0.0:8000"]
