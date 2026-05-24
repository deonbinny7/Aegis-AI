#!/usr/bin/env bash
# wait_for_db.sh

set -e

host="localhost"
port="5432"
user="postgres"

cmd="$@"

echo "Waiting for postgres at $host:$port..."

until pg_isready -h "$host" -p "$port" -U "$user"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
