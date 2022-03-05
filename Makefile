
.PHONY: docker-build docker-shell print-build-args \
	default build \
	print-docker-hub-image

SHELL=bash

default:
	echo pass

# vars for docker

REPO=adstewart

IMAGE_NAME=pandoc

IMAGE_VERSION=0.6

CTR_NAME=pandoc-ctr

# targets

print-image-name:
	@echo $(IMAGE_NAME)

print-image-version:
	@echo $(IMAGE_VERSION)

print-docker-hub-image:
	@printf '%s' "$(REPO)/$(IMAGE_NAME)"

docker-build:
	docker build \
		--cache-from $(REPO)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		-f Dockerfile \
		-t $(REPO)/$(IMAGE_NAME):$(IMAGE_VERSION) .

REMOVE_AFTER=--rm

docker-shell:
	-docker rm -f $(CTR_NAME)
	docker -D run $(REMOVE_AFTER) -it \
		--name $(CTR_NAME) \
		-v $$HOME/dev/:/home/dev \
		-v $$PWD:/work --workdir=/work \
		$(REPO)/$(IMAGE_NAME):$(IMAGE_VERSION)

