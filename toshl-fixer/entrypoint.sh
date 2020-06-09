#!/bin/bash

case $1 in
serve)
  exec gunicorn --bind :${PORT-8080} --workers 1 --threads 8 --reload toshl_fixer.app:app
  ;;
fetch-data)
  exec toshl-fixer fetch
  ;;
*)
  exec "$@"
  ;;
esac
