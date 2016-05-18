import os
import pwd
import shutil
import yaml

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install
from charms.reactive import hook, set_state, when, when_not, remove_state

import service_workload


@hook('install')
def install():
    apt_install(['nacl-tools'])

    # Stop in case the service was already installed and running. This is more
    # likely to happen when a subordinate is redeployed.
    manifest = service_workload.manifest()
    service = manifest["name"]
    if host.service_running(service):
        host.service_stop(service)

    service_workload.install()


@hook('upgrade-charm')
def upgrade():
    apt_install(['nacl-tools'])

    # TODO: get_state("service-workload.config")
    #       and compare with upgraded, remove old service if name has changed.
    manifest = service_workload.manifest()
    service = manifest["name"]
    need_restart = False
    if host.service_running(service):
        need_restart = True
        host.service_stop(service)
    service_workload.install()
    if need_restart:
        host.service_start(service)


@when('service-workload.start')
def restart_service_workload():
    remove_state('service-workload.start')
    manifest = service_workload.manifest()
    if host.service_running(manifest['name']):
        host.service_restart(manifest['name'])
    else:
        host.service_start(manifest['name'])
    set_state('service-workload.started')


@when('service-workload.stop')
def stop_service_workload():
    remove_state('service-workload.stop')
    manifest = service_workload.manifest()
    if host.service_running(manifest['name']):
        host.service_stop(manifest['name'])
