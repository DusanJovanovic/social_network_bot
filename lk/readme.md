# Django Social Network

Create Python virtual env:

Linux
```
python -m virtualenv env
```

Windows
```
python -m venv env
```

Activate vritual env:

Linux

```
source env/bin/activate
```

Windows

```
env/scripts/activate
```

Install requirements.txt
```
pip install -r requirements.txt
```

Run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
IMPORTANT!!!
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
After every run of script bots.py, delete db.sqlite3 and all files from migrations folder except __init__.py and run new migrations!
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
