COMMIT:=$(shell git rev-parse --verify --short HEAD)

build:
	docker build -t gcr.io/toshl-fixer/toshl-fixer:$(COMMIT) .

push:
	docker push gcr.io/toshl-fixer/toshl-fixer:$(COMMIT)

deploy:
	gcloud run deploy toshl-fixer --image gcr.io/toshl-fixer/toshl-fixer:$(COMMIT)

run-service:
	gcloud scheduler jobs run toshl-fixer

logs:
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=toshl-fixer" \
    --project toshl-fixer --limit 30 --order desc --format "value(textPayload)" | tac

update: build push deploy run-service
