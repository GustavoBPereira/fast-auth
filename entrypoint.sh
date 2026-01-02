#!/bin/sh
set -e

alembic upgrade head
exec uvicorn fast_auth.app:app --reload --host 0.0.0.0 --port 8000