#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.unregister as unreg
import pyp2p.register as reg

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
        reg.Register(server_address='p2pserver.cloudapp.net', port='5222').register('thing1234@iot.legrand.net','titi')

    def teardown(self):
        pass

    def test_register(self):
        self.unregister = unreg.Unregister(server_address='p2pserver.cloudapp.net', port='5222')
        self.unregister.unregister('thing1234@iot.legrand.net','titi')

