import base64
import os
import subprocess

from charmhelpers.core import hookenv


class AgentKey(object):
    ''''AgentKey represents a keypair that can be used for agent login'''
    
    def __init__(self):
        self.keydir = os.path.join(hookenv.charm_dir(), '..', '.agent-key') 
        if not os.path.exists(self.keydir):
            subprocess.check_call(('curvecpmakekey', self.keydir))
    
    def private_key(self):
        with open(os.path.join(self.keydir, '.expertsonly',
                               'secretkey'), 'rb') as f:       
            return str(base64.b64encode(f.read()), 'UTF-8')
    
    def public_key(self):
        with open(os.path.join(self.keydir, 'publickey'), 'rb') as f:
            return str(base64.b64encode(f.read()), 'UTF-8')
