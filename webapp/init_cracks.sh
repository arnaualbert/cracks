#!/bin/bash

source ../../venv/bin/activate
gunicorn --bind :8000 app:app --reload --access-logfile /var/log/nginx/cracks.access.log --error-logfile /var/log/nginx/cracks.error.log
