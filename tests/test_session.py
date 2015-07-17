#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
from pyp2p.register import Register
from pyp2p.unregister import Unregister
from pyp2p.session import P2pSession
from pyp2p.identifier import Identifier

import logging
import logging.handlers
import time

class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self,capacity):
        logging.handlers.BufferingHandler.__init__(self,capacity)

    def assert_logged(self,msg):
        logs = []
        for record in self.buffer:
            s = self.format(record)
            logs.append(s)
            if msg in s:
                return
        print(logs)
        assert False

    def assert_not_logged(self,msg):
        for record in self.buffer:
            s = self.format(record)
            if msg in s:
                assert False
        return
        

class TestSession:
 
    def setup(self):
        self.ident = Identifier(domain="iot.legrand.net").get()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '80'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"
        Register(server_address=self.server,
                 port=self.port).register(self.ident,self.password)

    def teardown(self):
        Unregister(server_address=self.server,
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


class TestPrivacy:
 
    def setup(self):
        self.alice_ident = Identifier(domain="iot.legrand.net").get()
        self.bob_ident = Identifier(domain="iot.legrand.net").get()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '80'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"

        reg = Register(server_address=self.server,
                     port=self.port)
        reg.register(self.alice_ident,self.password)
        reg.register(self.bob_ident,self.password)

    def teardown(self):
        unreg = Unregister(server_address=self.server,
                         port=self.port)
        unreg.unregister(self.alice_ident, self.password)
        unreg.unregister(self.bob_ident, self.password)
        
    def test_message_blocked(self):
        alice_session = P2pSession(server_address=self.server,
                             port=self.port)
        alice_session.start_session(jid=self.alice_ident, password=self.password)

        bob_session = P2pSession(server_address=self.server,
                             port=self.port)
        bob_session.start_session(jid=self.bob_ident, password=self.password)


        asserting_handler = AssertingHandler(800)
        logging.getLogger().addHandler(asserting_handler)

        alice_session.session_send(recipient=self.bob_ident, msg=self.test_msg)
        time.sleep(2)  # let the msg    
        asserting_handler.assert_not_logged(self.alice_ident+":"+self.test_msg)
        logging.getLogger().removeHandler(asserting_handler)


    def test_message_passed(self):
        alice_session = P2pSession(server_address=self.server,
                             port=self.port)
        alice_session.start_session(jid=self.alice_ident, password=self.password)

        bob_session = P2pSession(server_address=self.server,
                             port=self.port)
        bob_session.start_session(jid=self.bob_ident, password=self.password)

        # mutual subscription initiated by alice
        alice_session.subscribe(targetjid = self.bob_ident) 

        asserting_handler = AssertingHandler(1800)
        logger = logging.getLogger()
        logger.addHandler(asserting_handler)
        logger.setLevel(logging.INFO)
        time.sleep(2) # let subscription process occur
        alice_session.session_send(recipient=self.bob_ident, msg=self.test_msg)
        time.sleep(2)  # let the msg be logged    
        asserting_handler.assert_logged(self.alice_ident+":"+self.test_msg)
        logging.getLogger().removeHandler(asserting_handler)
