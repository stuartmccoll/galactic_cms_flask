#!/bin/bash

# Run a Flask development server
# --debug       # Run it in DEBUG mode.
# --reload      # Restart when a python file changed
python manage.py runserver -h 127.0.0.1 -p 5000 --debug --reload