# A Django Example Project

## Running

First ensure you have tox and Python 3.9 installation on your system, then clone the repo:

```bash
git clone https://github.com/LaurenceWarne/django-test
```

Create the necessary migrations:

```bash
tox -e py39 python manage.py makemigrations
```

Run the migrations:

```bash
tox -e py39 python manage.py migrate
```

Start a dev server:

```bash
tox -e py39 python manage.py runserver
```

Hit it!

```bash
curl -X POST http://127.0.0.1:8000/create-candidate -H "Content-Type: application/json" --data '{"ref":"12345678","name":"dave"}'
curl -X GET http://127.0.0.1:8000/get-candidate/12345678
```

## Testing

You can run the tests via:

```bash
tox -e py39
```
