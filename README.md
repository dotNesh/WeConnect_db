[![Maintainability](https://api.codeclimate.com/v1/badges/71f838efe01b737f374b/maintainability)](https://codeclimate.com/github/kmunene/WeConnect_db/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/kmunene/WeConnect_db/badge.svg?branch=reviews)](https://coveralls.io/github/kmunene/WeConnect_db?branch=reviews)
[![Build Status](https://travis-ci.org/kmunene/WeConnect_db.svg?branch=reviews)](https://travis-ci.org/kmunene/WeConnect_db)

# WeConnect

This is an API for WeConnect, a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to:

- Register an account and Login into it.
- Register, Update and delete a Business .
- View all Businesses.
- View One Business.
- Post Reviews to a business.
- View all Reviews to a business
- Change and Reset a users password
- Search and filter businesses

## Prerequisites

Python 3.6 or a later version
PostgresSQL

## Installation
Clone the repo.
```
$ git clone https://github.com/kmunene/WeConnect_db.git
```
and cd into the folder:
```
$ /WeConnect_db
```
## Virtual environment
Create a virtual environment:
```
python3 -m venv venv
```
Activate the environment
```
$ source venv/bin/activate
```
## Dependencies
Install package requirements to your environment.
```
pip install -r requirements.txt
```
## Env
Create a .env file in your root directory and activate it
```
source .env
```
## Database migration
Create two Databases:
- weconnect (production DB)
- weconnect_db (testing DB)

Run the following commands for each database:
```
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

```

## Testing
To set up unit testing environment:

```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:

```
$ nosetests --with-coverage
```

## Start The Server
To start the server run the following command
```
python run.py
```
The server will run on port: 5000

## Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```


### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/auth/v2/register | POST | Creates a user account | FALSE
| /api/auth/v2/login | POST | Logs in a user | TRUE
| /api/auth/v2/logout | POST | Logs out a user | TRUE
| /api/auth/v2/reset-password | POST | Reset user password | TRUE
| /api/auth/v2/change-password | POST | Change user password | TRUE
| /api/v2/businesses | POST | Register a business | TRUE
| /api/v2/businesses | GET | Retrieves all businesses | FALSE 
| /api/v2/businesses/{businessid} | GET | Get a business | FALSE
| /api/v2/businesses/{businessid} | PUT | Update a business profile | TRUE
| /api/v2/businesses/{businessid} | DELETE | Delete a business | TRUE
| /api/v2/businesses/{businessid}/reviews | POST | Post a review on a business | TRUE
| /api/v2/businesses/{businessid}/reviews | GET | Get all reviews to a business | FALSE
| /api/v2/businesses/search | GET | Search and filter businesses | FALSE

## Pagination

The API enables pagination by passing in *page* and *limit* as arguments in the request url as shown in the following example:

```
http://127.0.0.1:5000//api/v2/businesses?page=1&limit=10

```

## Searching and filtering
The API implements searching based on the name using a GET parameter *q* as shown below:
```
http://127.0.0.1:5000//api/v2/businesses/search?name=Andela
```
One can also filter a search result further based on the business Location and category as shown:
```
http://127.0.0.1:5000//api/v2/businesses/search?name=Andela&category=software&location=Nairobi
```

## API Documentation

## Authors

* **Kariuki Kelvin** - [kmunene](https://github.com/kmunene)

## Acknowledgments
* Flevian Kanaiza
* **Stephen Muthama** - [muthash](https://github.com/muthash)
* Linnette Wanjiru
