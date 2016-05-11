
CHARM_REPO := $(shell cd ../..; pwd)

CACHE_GOPATH=$(CHARM_REPO)/cache/gopath/mongodb_exporter

BINS=files/mongodb_exporter

.PHONY: all
all: $(CHARM_REPO)/trusty/mongodb-exporter/metadata.yaml

$(CHARM_REPO)/trusty/mongodb-exporter/metadata.yaml: $(BINS)
	JUJU_REPOSITORY=$(CHARM_REPO) charm build -n mongodb-exporter -l debug

.PHONY: cache
cache: $(CACHE_GOPATH)/src/github.com/dcu/mongodb_exporter

files/mongodb_exporter: $(CACHE_GOPATH)/src/github.com/dcu/mongodb_exporter
	GOPATH=$(CACHE_GOPATH) go build -o $@ github.com/dcu/mongodb_exporter

$(CACHE_GOPATH)/src/github.com/dcu/mongodb_exporter:
	GOPATH=$(CACHE_GOPATH) go get -u github.com/dcu/mongodb_exporter

.PHONY: files-clean
files-clean:
	$(RM) $(BINS)

.PHONY: charm-clean
charm-clean:
	$(RM) -r $(CHARM_REPO)/trusty/mongodb-exporter

.PHONY: cache-clean
cache-clean:
	$(RM) -r $(CACHE_GOPATH)

.PHONY: clean
clean: files-clean charm-clean

