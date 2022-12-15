start:
	poetry run uvicorn task_bot.main:app --reload --port=8443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem

lint:
	poetry run flake8 src tests

compose:
	docker-compose up -d --build

compose-down:
	docker-compose down

migrate:
	docker-compose exec app alembic upgrade head

