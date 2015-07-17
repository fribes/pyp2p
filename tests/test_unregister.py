#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.unregister as unreg
import pyp2p.register as reg
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


class TestUnregister:
 
    def setup(self):
        self.asserting_handler = AssertingHandler(200)
        logging.getLogger().addHandler(self.asserting_handler)
        self.ident = Identifier(domain="iot.legrand.net").get()
        reg.Register(server_address='p2pserver.cloudapp.net', port='80').register(self.ident,'titi')
        self.asserting_handler.assert_logged("Account created")


    def teardown(self):
        logging.getLogger().removeHandler(self.asserting_handler)

    def test_unregister(self):
        self.unregister = unreg.Unregister(server_address='p2pserver.cloudapp.net', port='80')
        self.unregister.unregister(self.ident,'titi')
        self.asserting_handler.assert_logged("User removed")

