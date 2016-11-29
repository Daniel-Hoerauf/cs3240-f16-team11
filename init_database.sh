#!/bin/bash

python manage.py migrate

python manage.py loaddata site_manager.json
