# mongodb-exporter

This project builds a reactive layered charm for [mongodb_exporter](https://github.com/dcu/mongodb_exporter).

## Build

In this directory, with `$JUJU_REPOSITORY` set:

    $ make clean all

Will compile `mongodb_exporter` from latest Github master and build the charm
with the static binary included.

## Usage

This charm is a subordinate that adds an HTTP metric scrape endpoint to MongoDB.

    $ juju deploy mongodb
    $ juju deploy prometheus
    $ juju deploy cs:~cmars/trusty/mongodb-exporter
    $ juju add-relation mongodb mongodb-exporter
    $ juju add-relation mongodb-exporter prometheus

This will expose HTTP operational metrics on all mongodb units, which
prometheus will pull from.

## License

Copyright 2016 Casey Marshall. Distributed under the [Apache Public License 2.0](copyright).

## TODO

Currently there are no configuration options, and `mongodb_exporter` assumes it
can connect to `localhost:27017` when deployed onto a mongodb service.

Only trusty is supported, mostly because there isn't a production-ready mongodb
charm ready for xenial yet.

Alternative methods for delivering the `mongodb_exporter` binary.
