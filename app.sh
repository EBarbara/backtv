#!/bin/bash
gunicorn url:app --bind=0.0.0.0:8080 --log-file - --access-logfile -
