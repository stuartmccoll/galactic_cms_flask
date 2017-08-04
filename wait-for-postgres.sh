#!/bin/sh

postgres_host="$1"
postgres_port="$2"

shift
cmd="$@"

until pg_isalready -h "$postgres_host" -p "$postgres_port" -q; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# run the command
exec $cmd