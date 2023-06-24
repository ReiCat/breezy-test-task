# Breezy test task

## Steps to run locally

To run this project the Python 3+ and PostgreSQL 14.7 is required.

### Create database & user with password

`$ sudo -u postgres psql`

`postgres=# create database breezy_test_db;`

`postgres=# create user breezy_test_user with encrypted password 'breezy_test_password';`

`postgres=# grant all privileges on database breezy_test_db to breezy_test_user;`

`postgres=# \q`

### Create virtual environment for the project

`$ virtualenv -p python3 venv`

### Activate it

`$ source venv/bin/activate`

### Install all the requirements

`$ pip install -r requirements.txt`

### Apply database migrations

`$ python manage.py migrate`

### Run the server

`$ python manage.py runserver`
