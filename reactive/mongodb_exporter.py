from charms.reactive import when, remove_state, hook
from charmhelpers.core import hookenv


@hook('install')
def install():
    hookenv.open_port(9001)


@when('target.available')
def target_available(p):
    p.configure(9001)
    remove_state('target.available')
