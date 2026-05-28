.PHONY: build up down logs shell-backend

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

status:
	docker compose ps

# Run the supervisor natively for maximum speed
run-native:
	env PYTHONPATH=.:backend ./venv/bin/python3 backend/main.py

# Run the supervisor locally (requires venv)
run-local:
	source venv/bin/activate && python backend/main.py
