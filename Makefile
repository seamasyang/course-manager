.PHONY: dev-backend dev-frontend dev build install-backend install-frontend start-backend start-frontend

# Backend
install-backend:
	cd backend && pip install -r requirements.txt

dev-backend:
	cd backend && uvicorn app.main:app --reload

# Frontend
install-frontend:
	cd frontend && npm install

dev-frontend:
	cd frontend && npm run dev

# Run everything with Docker
dev:
	docker compose up

build:
	docker compose build

# Install all dependencies
install: install-backend install-frontend

# Run both dev servers locally
dev-local:
	@echo "Run 'make dev-backend' and 'make dev-frontend' in separate terminals"