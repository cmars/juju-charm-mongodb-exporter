import os
import shutil
import yaml

from charmhelpers.core import hookenv
from charmhelpers.core.host import add_group, adduser
from charmhelpers.core.templating import render
from charms.reactive import set_state

from service_workload.dist import install_binary, binary_file


def manifest():
    with open(os.path.join(hookenv.charm_dir(), "service-workload.yaml")) as f:
        return yaml.load(f)


def install():
    m = manifest()
    install_binary(m)
    setup_user(m)
    write_upstart(m)
    set_state('service-workload.available')


def config_file(deployment):
    if deployment is None:
        deployment = 'devel'
    d = {'deployment': deployment}
    d.update(manifest())
    return '/srv/%(name)s/%(deployment)s/etc/%(binary)s/config.yaml' % d


def setup_user(m):
    name = m['name']
    add_group(name)
    adduser(name, system_user=True)


def write_upstart(m):
    config = hookenv.config()
    settings = {'config_file': config_file(config.get('deployment'))}
    settings.update(config)
    settings.update(m)
    args = m['args'] % settings
    render(source="upstart",
        target="/etc/init/%s.conf" % (m['name']),
        owner="root",
        perms=0o644,
        context={
            "manifest": m,
            "config": config,
            "args": args,
            "installed_binary": binary_file(m),
        })
