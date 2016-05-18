import glob
import os
import shutil
import yaml

from charmhelpers.core import hookenv


def binary_file(m):
    return '/srv/%(name)s/dist/charm/bin/%(binary)s' % m


def install_binary(m):
    install_dir = os.path.dirname(binary_file(m))
    os.makedirs(install_dir, mode=0o755, exist_ok=True)
    for charm_binary in glob.glob("%s/files/*" % (hookenv.charm_dir())):
        installed_binary = os.path.join(install_dir, os.path.basename(charm_binary))
        shutil.copyfile(charm_binary, installed_binary)
        os.chmod(installed_binary, 0o755)
