test-create-db:
	@echo "Creating Hame database..."
	curl -XPOST "http://localhost:8081/2015-03-31/functions/function/invocations" -d '{"action" : "create_db"}'

test-migrate-db:
	@echo "Migrating Hame database..."
	curl -XPOST "http://localhost:8081/2015-03-31/functions/function/invocations" -d '{"action" : "migrate_db"}'

test-koodistot:
	@echo "Loading Koodistot data..."
	curl -XPOST "http://localhost:8082/2015-03-31/functions/function/invocations" -d '{}'
	curl -XPOST "http://localhost:8085/2015-03-31/functions/function/invocations" -d '{}'

test-ryhti-validate:
	@echo "Validating database contents with Ryhti API..."
	curl -XPOST "http://localhost:8083/2015-03-31/functions/function/invocations" -d '{"action": "validate_plans"}'

pytest-fail:
	pytest --maxfail=1

up:
	docker compose -f docker-compose.dev.yml up -d

stop:
	docker compose -f docker-compose.dev.yml stop

down:
	docker compose -f docker-compose.dev.yml down -v

build-lambda:
	docker compose -f docker-compose.dev.yml build db_manager koodistot_loader ryhti_client mml_loader

revision:
	alembic revision --autogenerate -m "$(name)"; \
