## Overview
it is a simple <b>Flask</b> web project that consists of <b>Welcome</b>, <b>Sign_up</b>, <b>Sign_in</b> & <b>User_home</b> pages.

## Requirements
```
Python3, MySQL-server, Flask
```

## Setup & Installation
### 1) Setup your database: 
* After the installation of MySQL server, run it.
```
mysql -u USERNAME -p PASSWORD
```
* Create your database then use it.
```
mysql> CREATE DATABASE test_accounts;
mysql> use test_accounts;
```
### 2) Create the table schema:
* Change your directory to <b>test_task_digzilla</b>, then run <b>Python3</b> shell.
* Run this code in the shell.
```python

from app import db
db.create_all()
```
* Exit the <b>Python</b> shell.

### 3) Edit the code with your MySQL server credentials:
* Edit this line of code in <b>app.py</b>
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@localhost/test_accounts'
```
