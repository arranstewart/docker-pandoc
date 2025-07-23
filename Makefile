
.PHONY: docker-build docker-shell print-build-args \
	default build \
	print-docker-hub-image

SHELL=bash

default:
	echo pass

METADATA_FILE := METADATA.env

# e.g. adstewart
IMAGE_NAMESPACE := $(shell grep '^IMAGE_NAMESPACE=' $(METADATA_FILE) | cut -d= -f2-)

# e.g. 0.7
IMAGE_VERSION := $(shell grep '^IMAGE_VERSION=' $(METADATA_FILE) | cut -d= -f2-)

# e.g. pandoc
IMAGE_NAME    := $(shell grep '^IMAGE_NAME=' $(METADATA_FILE) | cut -d= -f2-)



# quick and dirty build

PLATFORMS = linux/amd64,linux/arm64
#PLATFORMS = linux/amd64


# uses the builder `multiarch-builder` - we assume
# it's been created as per the README.
docker-build:
	docker buildx build \
		--progress=plain \
		--builder=multiarch-builder \
		--cache-from $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		--platform $(PLATFORMS) \
		-f Dockerfile \
		-t $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		-t $(IMAGE_NAMESPACE)/$(IMAGE_NAME):latest \
		--push \
		.

CTR_NAME = pandoc-ctr

REMOVE_AFTER = --rm

#PLATFORM_TO_RUN = linux/amd64
PLATFORM_TO_RUN = linux/arm64

docker-shell:
	-docker rm -f $(CTR_NAME)
	docker -D run $(REMOVE_AFTER) -it \
		--name $(CTR_NAME) \
		--platform $(PLATFORM_TO_RUN) \
		-v $$HOME/dev/:/home/dev \
		-v $$PWD:/work --workdir=/work \
		$(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)

