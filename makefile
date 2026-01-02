COMPOSE ?= docker compose
SERVICE ?= api

.PHONY: run down build exec test alembic-revision alembic-upgrade

run:
	$(COMPOSE) up

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

exec:
	$(COMPOSE) exec $(SERVICE) sh

test:
	$(COMPOSE) exec $(SERVICE) pytest

alembic-revision:
	$(COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "$(msg)"

alembic-upgrade:
	$(COMPOSE) exec $(SERVICE) alembic upgrade head
