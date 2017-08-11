IMGNAME=sdelrio/claymore-exporter
VERSION=:$(TAG)
TESTIP=192.168.1.34
TESTPORT=8601
BASE_X86=jfloff/alpine-python
BASE_ARM=resin/raspberry-pi-alpine-python
.PHONY: all build run

all: build run

build:
			@docker build --build-arg BASE_IMAGE=$(BASE_X86) -t $(IMGNAME)$(VERSION) --rm . && echo Buildname: $(IMAGENAME):$(VERSION)
			@docker build --build-arg BASE_IMAGE=$(BASE_ARM) -t $(IMGNAME)-arm$(VERSION) --rm -f Dockerfile.arm . && echo Buildname: $(IMAGENAME):$(VERSION)

run:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME)$(VERSION)

runarm:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME)-arm$(VERSION)
