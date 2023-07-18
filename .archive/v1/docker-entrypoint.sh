#!/bin/sh
flask db init
flask db migrate
flask db upgrade
python -m flask run --host=0.0.0.0
