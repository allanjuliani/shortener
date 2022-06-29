# URL Shortener - Dev

#### Ubuntu 20.04 Dependencies
```commandline
sudo apt-get install git build-essential python3-virtualenv libxml2-dev libxslt1-dev libevent-dev python3-dev libsasl2-dev libmysqlclient-dev libjpeg-dev libffi-dev libssl-dev -y
```

#### Create the Virtualenv
```commandline
virtualenv .venv
```

#### Activate Virtualenv
```commandline
source .venv/bin/activate
```

#### Install Python Dependencies

```commandline
pip install -r requirements.txt
```
#### Export env variables
```commandline
export $(cat .env.example | xargs)
```
#### Install Database

```commandline
./manage.py migrate --settings=shortener.settings_dev
```

#### Create admin user

```commandline
./manage.py createsuperuser --noinput --settings=shortener.settings_dev
```

#### Test the application

```commandline
pytest -v apps/
```

#### Show coverage

```commandline
pytest apps/ --cov=apps/
```

#### Running the application

```commandline
./manage.py runserver 0.0.0.0:8000 --settings=shortener.settings_dev
```

#### Admin URL to access on browser
http://localhost:8000/admin/
