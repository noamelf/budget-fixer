COMMIT:=$(shell git rev-parse --verify HEAD)

.PHONY: build
build:
	docker build -t gcr.io/toshl-fixer/toshl-fixer:$(COMMIT) .

.PHONY: push
push:
	docker push gcr.io/toshl-fixer/toshl-fixer:$(COMMIT)

.PHONY: deploy
deploy:
	gcloud run deploy toshl-fixer --image gcr.io/toshl-fixer/toshl-fixer:$(COMMIT)

run-service:
	gcloud scheduler jobs run toshl-fixer

update: build push deploy run-service
