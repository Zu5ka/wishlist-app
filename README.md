# Wishlist app

This is a web app that enables users to *make* and edit their own wishlists and *share* them with other users.<br/>
The owner of a wishlist can *archive* and *delete* it and *claim* and *delete* the items on it. <br/>
The user with whom the wishlist is shared can *reserve* items on it lists. The owner of the list however, doesn't see which items are reserved. <br/>

This app should help people to share what they wish for eg. birthdays without ruining the joy of a surprise - the owners don't know which items will be given to them and by whom. It also prevents duplicates and the owner doesn't push anyone into giving them a specific thing.

## Necessary dependencies

- flask
- Flask-SQLAlchemy
- FLask-Login
- waitress
- pytest
- pytest-flask

Read requirements.txt for further details.

this app was written with python3.11

## How to start

1. Prepare a directory for this project, eg. `mkdir wishlist-app` and jump in `cd wishlist-app`.
1. Clone this repository: `git clone git@gitlab.fit.cvut.cz:BI-PYT/B232/zuskokat.git`
1. Create a virtual environment: `python3.11 -m venv venv-wishlist`
1. Activate the venv: `source venv-wishlist/bin/activate`
1. Jump in the project directory: `cd zuskokat`
1. Install all required python packages `pip install -r requirements.txt`  
1. Run the app `python run.py`  

```
options:
  -h, --help       show this help message and exit
  --port PORT      Port on which the app should run (default 5000)
  --prod           Run in production mode
  --db-url DB_URL  Database URL (default sqlite:///wishlist.db)
  --secret SECRET  Secret key (default: random)
  --host HOST      Host (default: 127.0.0.1)
```

The app will run on host (default: 127.0.0.1)

## How to run tests from CLI

1. Activate the venv: `source venv-wishlist/bin/activate`
1. Jump in your materials: `cd zuskokat`
2. Run the tests: `pytest tests/test_app.py`
