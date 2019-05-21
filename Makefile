current_dir = $(shell pwd)

PROJECT = lookout

DOCKERFILES = Dockerfile:$(PROJECT)
DOCKER_ORG = "srcd"

# Including ci Makefile
CI_REPOSITORY ?= https://github.com/src-d/ci.git
CI_BRANCH ?= v1
CI_PATH ?= .ci
MAKEFILE := $(CI_PATH)/Makefile.main
$(MAKEFILE):
	git clone --quiet --depth 1 -b $(CI_BRANCH) $(CI_REPOSITORY) $(CI_PATH);
-include $(MAKEFILE)

.PHONY: check
check:
	! (grep -R /tmp lookout/core/tests)
	flake8 --count
	pylint lookout

.PHONY: test
test:
	python3 -m unittest discover

.PHONY: docs
docs:
	cd docs && python3 -m sphinx -M html . build

.PHONY: docker-build
docker-build:
	docker build -t srcd/lookout-sdk-ml .

.PHONY: docker-test
docker-test: docker-build
	docker ps | grep bblfshd  # bblfsh server should be running
	docker run --rm -it --network host --entrypoint python3 -w /lookout-sdk-ml \
		-v $(current_dir)/.git:/lookout-sdk-ml/.git \
		srcd/lookout-sdk-ml -m unittest discover

.PHONY: bblfsh-start
bblfsh-start:
	! docker ps | grep bblfshd # bblfsh server should not be running already
	docker run -d --name style_analyzer_bblfshd --privileged -p 9432\:9432 bblfsh/bblfshd\:v2.11.8
	docker exec style_analyzer_bblfshd bblfshctl driver install \
		javascript docker://bblfsh/javascript-driver\:v2.7.1
