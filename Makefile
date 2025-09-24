install:
	uv sync


dev:
	uv run flask --debug --app page_analyzer:app run --port=8000


PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


build:
	./build.sh


render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


lint:
	ruff check


test:
	uv run pytest -v
