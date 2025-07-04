

.PHONY: run migrate upgrade 

run:
	python src/main.py


migrate:
	alembic revision --autogenerate -m "$(m)"

upgrade:
	alembic upgrade head
