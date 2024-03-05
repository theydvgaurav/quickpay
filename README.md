
# QuickPay

A Razorpay payment service developed using Django, PSQL.



## Project Setup

Clone the repository: 
```bash
  git clone https://github.com/theydvgaurav/quickpay
```

Create a python3.11 virtual environment and activate it:
```bash
  cd quickpay
  python3.11 -m venv env
  source env/bin/activate
```
Install all the requirements: 
```bash
  pip install requirements.txt
```
Adding environment variables and setting them:\
Create a file named local.env and add the follwing variables\
DATABASE_USERNAME=<str>\
DATABASE_HOST=<str>\
DATABASE_NAME=<str>\
DATABASE_PASSWORD=<str>\
JWT_ADMIN_ENCODE_SECRET=<str>\
RAZORPAY_API_KEY=<str>\
RAZORPAY_API_SECRET=<str>
```bash
  set -a && source local.env && set +a
```
Apply the migrations:
```bash
  python manage.py migrate
```
Start the server:
```bash
  python manage.py runserver
```