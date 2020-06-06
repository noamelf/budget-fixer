deploy-fixer:
	gcloud run deploy toshl-fixer --image gcr.io/toshl-fixer/toshl-fixer:latest

deploy-classifier:
	gcloud run deploy expenses-classifier --image gcr.io/toshl-fixer/expense-classifier:latest

deploy-all: deploy-classifier deploy-fixer

run-service:
	gcloud scheduler jobs run toshl-fixer-tag

logs-fixer:
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=toshl-fixer" \
    --project toshl-fixer --limit 30 --order desc --format "value(textPayload)" | tac

logs-classifier:
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=expenses-classifier" \
    --project toshl-fixer --limit 30 --order desc --format "value(textPayload)" | tac

logs-all: logs-classifier logs-fixer

update: deploy-all run-service
