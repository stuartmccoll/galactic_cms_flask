#!/bin/sh

set -e

shift
cmd="$@"

until psql -h "db-galactic-cms" -U "postgres" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd