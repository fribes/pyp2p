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

class TestSession:
 
    def setup(self):
        self.ident = Identifier(domain="iot.legrand.net").get_identifier()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '80'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"
        Register(server_address=self.server,
                 port=self.port).register(self.ident,self.password)
        self.from_jid = None
        self.msg_body = None


    def teardown(self):
        Unregister(server_address=self.server,
                   port=self.port).unregister(self.ident, self.password)

    def callback(self, from_jid, msg_body):
        self.from_jid = from_jid
        self.msg_body = msg_body

    def test_message_to_myself(self):
        session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.ident, 
                             password=self.password)

        session.set_msg_callback(cb=self.callback)

        session.session_send(recipient=self.ident, msg=self.test_msg)
        time.sleep(1)  #  let the message transit    
        assert self.from_jid == self.ident
        assert self.msg_body == self.test_msg


class TestPrivacy:
 
    def setup(self):
        self.alice_ident = Identifier(domain="iot.legrand.net").get_identifier()
        self.bob_ident = Identifier(domain="iot.legrand.net").get_identifier()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '80'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"

        reg = Register(server_address=self.server,
                     port=self.port)
        reg.register(self.alice_ident,self.password)
        reg.register(self.bob_ident,self.password)
        self.from_jid = None
        self.msg_body = None

    def teardown(self):
        unreg = Unregister(server_address=self.server,
                         port=self.port)
        unreg.unregister(self.alice_ident, self.password)
        unreg.unregister(self.bob_ident, self.password)

    def callback(self, from_jid, msg_body):
        self.from_jid = from_jid
        self.msg_body = msg_body

    def test_message_blocked_not_in_roster(self):
        alice_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.alice_ident,
                              password=self.password)

        bob_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.bob_ident,
                              password=self.password)

        bob_session.set_msg_callback(cb=self.callback)

        alice_session.session_send(recipient=self.bob_ident, msg=self.test_msg)
        time.sleep(1)  #  let the message transit    
        assert self.from_jid == None
        assert self.msg_body == None


    def test_message_blocked_bob_reject(self):
        alice_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.alice_ident,
                              password=self.password)

        bob_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.bob_ident,
                              password=self.password)

        alice_session.authorize_subscriptions()

        # mutual subscription initiated by alice
        alice_session.subscribe(targetjid = self.bob_ident) 
        bob_session.set_msg_callback(cb=self.callback)

        time.sleep(1) # let subscription process occur
        alice_session.session_send(recipient=self.bob_ident, msg=self.test_msg)
        time.sleep(1)  #  let the message transit    
        assert self.from_jid == None
        assert self.msg_body == None

    def test_message_passed(self):
        alice_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.alice_ident,
                              password=self.password)

        bob_session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.bob_ident,
                              password=self.password)

        alice_session.authorize_subscriptions()
        bob_session.authorize_subscriptions()

        # mutual subscription initiated by alice
        alice_session.subscribe(targetjid = self.bob_ident) 

        bob_session.set_msg_callback(cb=self.callback)

        time.sleep(1) # let subscription process occur
        alice_session.session_send(recipient=self.bob_ident, msg=self.test_msg)
        time.sleep(1)  # let the msg be logged    
        assert self.from_jid == self.alice_ident
        assert self.msg_body == self.test_msg

class TestMessageCallback:
 
    def setup(self):
        self.ident = Identifier(domain="iot.legrand.net").get_identifier()
        self.server = 'p2pserver.cloudapp.net'
        self.port = '80'
        self.password = 'titi'
        self.test_msg = "il n'y a pas de hasard"
        Register(server_address=self.server,
                 port=self.port).register(self.ident,self.password)
        self.from_jid = None
        self.msg_body = None

    def teardown(self):
        Unregister(server_address=self.server,
                   port=self.port).unregister(self.ident, self.password)
        
    def callback(self, from_jid, msg_body):
        self.from_jid = from_jid
        self.msg_body = msg_body

    def test_message_callback(self):
        session = P2pSession(server_address=self.server,
                             port=self.port,
                             jid=self.ident,
                              password=self.password)
        
        session.set_msg_callback(cb=self.callback)

        session.session_send(recipient=self.ident, msg=self.test_msg)
        time.sleep(2)  # let the msg    

        assert self.from_jid == self.ident
        assert self.msg_body == self.test_msg
