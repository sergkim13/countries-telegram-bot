install:
	poetry install

test:
	poetry run pytest -vv

hooks:
	poetry run pre-commit run --all-files

run-bot:
	poetry run python manage.py runbot

server:
	poetry run python manage.py runserver

compose:
	docker compose up -d

stop:
	docker compose down

migrate:
	poetry run python manage.py migrate
