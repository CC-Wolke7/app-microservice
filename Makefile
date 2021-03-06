NAME = app-microservice
REGISTRY = gcr.io/wolke-sieben-fs
VERSION = $(shell git describe --tags --dirty --always --long)

PROJECT_ROOT = $(shell pwd)

DEV_IMAGE_NAME = ${NAME}-dev
DEV_CONTAINER_NAME = ${DEV_IMAGE_NAME}
DEV_PORT = 3000

TEST_IMAGE_VERSION = ${VERSION}-dev

.PHONY: test-image push-test-image deploy

test-image:
	docker build -t ${NAME} .

push-test-image: test-image
	docker tag ${NAME}:latest ${NAME}:${TEST_IMAGE_VERSION}
	docker tag ${NAME}:latest ${REGISTRY}/${NAME}:${TEST_IMAGE_VERSION}
	docker push ${REGISTRY}/${NAME}:${TEST_IMAGE_VERSION}

deploy:
	gcloud beta run services replace app.service.yaml --platform managed --region europe-west3

collectstatic:
	docker run --rm -e DJANGO_ENVIRONMENT='minimal' -v ${PROJECT_ROOT}/static:/app/app_microservice/app_microservice/static --entrypoint python ${NAME} manage.py collectstatic --no-input
