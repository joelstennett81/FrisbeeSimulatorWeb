#!/bin/bash
python manage.py migrate && python manage.py collectstatic collectstatic && gunicorn --workers 2 app.wsgi