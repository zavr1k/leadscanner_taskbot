start:
	poetry run uvicorn task_bot.main:app --reload --port=8443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
lint:
	poetry run flake8 src tests
