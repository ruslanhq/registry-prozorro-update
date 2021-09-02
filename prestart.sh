#! /usr/bin/env bash

# Let the DB start
sleep 20;
# Run migrations
alembic upgrade head