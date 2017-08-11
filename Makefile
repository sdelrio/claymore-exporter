TAG ?= latest
IMGNAME=sdelrio/claymore-exporter
TESTIP=192.168.1.34
TESTPORT=8601
BASE_X86=jfloff/alpine-python
BASE_ARM=resin/raspberry-pi-alpine-python
.PHONY: all build run

all: build run

build:
			@docker build --build-arg BASE_IMAGE=$(BASE_X86) -t $(IMGNAME):$(TAG) --rm . && echo Buildname: $(IMAGENAME):$(TAG)
			@docker build --build-arg BASE_IMAGE=$(BASE_ARM) -t $(IMGNAME)-arm:$(TAG) --rm -f Dockerfile.arm . && echo Buildname: $(IMAGENAME):$(TAG)

run:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME):$(TAG)

runarm:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME)-arm:$(TAG)
