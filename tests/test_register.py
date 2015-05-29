#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.register as reg
import pyp2p.unregister as unreg

import logging
import logging.handlers

class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self,capacity):
        logging.handlers.BufferingHandler.__init__(self,capacity)

    def assert_logged(self,msg):
        for record in self.buffer:
            s = self.format(record)
            if msg in s:
                return
        assert False


class TestRegister:
 
    def setup(self):
        self.register = reg.Register(server_address='p2pserver.cloudapp.net', port='5222')
 
    def teardown(self):
        unreg.Unregister(server_address='p2pserver.cloudapp.net', port='5222').unregister('thing1234@iot.legrand.net','titi')

    def test_register(self):
        assert self.register.register('thing1234@iot.legrand.net','titi')

    def test_register_again(self):
        assert self.register.register('thing1234@iot.legrand.net','titi')
        
    def test_register_conflict(self):
        asserting_handler = AssertingHandler(200)
        logging.getLogger().addHandler(asserting_handler)
        assert self.register.register('thing1234@iot.legrand.net','titi')
        self.register.register('thing1234@iot.legrand.net','toto')
        asserting_handler.assert_logged("Could not register account")
        logging.getLogger().removeHandler(asserting_handler)

    def test_register_twice(self):
        assert self.register.register('thing1234@iot.legrand.net','titi')
        assert self.register.register('thing1234@iot.legrand.net','titi')
