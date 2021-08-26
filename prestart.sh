#! /usr/bin/env bash

# Let the DB start
sleep 30;
# Run migrations
alembic upgrade head