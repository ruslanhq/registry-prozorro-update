#! /usr/bin/env bash

# Let the DB start
sleep 40;
# Run migrations
alembic upgrade head