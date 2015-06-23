#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import pyp2p.register as reg
import pyp2p.unregister as unreg
from pyp2p.session import P2pSession
from pyp2p.identifier import Identifier

import logging
import logging.handlers
import time

class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self,capacity):
        logging.handlers.BufferingHandler.__init__(self,capacity)

    def assert_logged(self,msg):
        for record in self.buffer:
            s = self.format(record)
            if msg in s:
                return
        assert False


class TestSession:
 
    def setup(self):
        self.ident = Identifier(domain="iot.legrand.net").get()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '5222'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"
        reg.Register(server_address=self.server,
                     port=self.port).register(self.ident,self.password)

    def teardown(self):
        unreg.Unregister(server_address=self.server,
                         port=self.port).unregister(self.ident, self.password)
        
    def test_message_to_myself(self):
        session = P2pSession(server_address=self.server,
                             port=self.port)
        session.start_session(jid=self.ident, password=self.password)

        asserting_handler = AssertingHandler(800)
        logging.getLogger().addHandler(asserting_handler)

        session.session_send(recipient=self.ident, msg=self.test_msg)
        time.sleep(2)  # let the msg    
        asserting_handler.assert_logged(self.ident+":"+self.test_msg)
        logging.getLogger().removeHandler(asserting_handler)
