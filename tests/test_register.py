#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.register as reg
import pyp2p.unregister as unreg
from pyp2p.identifier import Identifier

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
        self.register = reg.Register(server_address='p2pserver.cloudapp.net', port='80')
        self.ident = Identifier(domain="iot.legrand.net").get()

    def teardown(self):
        unreg.Unregister(server_address='p2pserver.cloudapp.net', port='80').unregister(self.ident,'titi')

    def test_register(self):
        assert self.register.register(self.ident,'titi')

    def test_register_again(self):
        assert self.register.register(self.ident,'titi')
        
    def test_register_conflict(self):
        asserting_handler = AssertingHandler(200)
        logging.getLogger().addHandler(asserting_handler)
        assert self.register.register(self.ident,'titi')
        self.register.register(self.ident,'toto')
        asserting_handler.assert_logged("Could not register account")
        logging.getLogger().removeHandler(asserting_handler)

    def test_register_twice(self):
        assert self.register.register(self.ident,'titi')
        assert self.register.register(self.ident,'titi')
