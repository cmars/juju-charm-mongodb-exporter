from charms.reactive import when, when_not, set_state, remove_state, hook
from charmhelpers.core import hookenv


@hook('install')
def install():
    hookenv.open_port(9001)


@when('service-workload.available')
@when_not('service-workload.started')
def start():
    set_state('service-workload.start')


@when('target.available')
def target_available(p):
    p.configure(9001)
    remove_state('target.available')
