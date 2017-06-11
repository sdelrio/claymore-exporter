IMGNAME=sdelrio/claymore-exporter
VERSION=:$(TAG)
TESTIP=192.168.1.34
TESTPORT=8601
.PHONY: all build run

all: build run

build:
			@docker build -t $(IMGNAME)$(VERSION) --rm . && echo Buildname: $(IMAGENAME):$(VERSION)
			@docker build -t $(IMGNAME)-arm$(VERSION) --rm -f Dockerfile.arm . && echo Buildname: $(IMAGENAME):$(VERSION)

run:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME)$(VERSION)

runarm:
			docker run --rm -ti -p $(TESTPORT):$(TESTPORT) $(IMGNAME)-arm$(VERSION)
