#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.register as reg

class TestRegister:
 
    def setup(self):
        self.register = reg.Register(server_address='p2pserver.cloudapp.net', port='5222')
 
    def teardown(self):
        pass
 
    def test_register(self):
        assert self.register.register('thing1234@iot.legrand.net','titi')
        
 
