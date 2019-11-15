NS ?= docker.io/krishnabigdata
VERSION ?= latest
IMAGE_NAME ?= taxi_data_analysis

.PHONY: build push

build:
	docker build -t $(NS)/$(IMAGE_NAME):$(VERSION) -f Dockerfile .

push:
	docker push $(NS)/$(IMAGE_NAME):$(VERSION)

default: build