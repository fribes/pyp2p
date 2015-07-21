#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
from pyp2p.identifier import Identifier 

class TestIdentifier:
 
    def setup(self):
        pass
 
    def teardown(self):
        pass

    def test_random(self):
        domain = "iot.legrand.net"
        ident = Identifier(domain=domain)

        uid = ident.get_identifier()
        assert domain in uid
        assert len(uid) == 36 + 1 + len(domain) 

    def test_prefixed(self):
        domain = "iot.legrand.net"
        prefix = "eliot-"
        ident = Identifier(domain=domain,prefix=prefix)

        uid = ident.get_identifier()
        assert domain in uid
        assert uid.find(prefix)==0
        assert len(uid) == len(prefix) + 12 + 1 + len(domain) 

    def test_password(self):
        domain = "iot.legrand.net"
        prefix = "eliot-"
        ident = Identifier(domain=domain)

        password = ident.get_password()
        assert len(password) == 16 

    def test_password_bigger_length(self):
        domain = "iot.legrand.net"
        ident = Identifier(domain=domain, pass_length=18)

        password = ident.get_password()
        assert len(password) == 18

    def test_password_shorter_length(self):
        domain = "iot.legrand.net"
        ident = Identifier(domain=domain, pass_length=10)

        password = ident.get_password()
        assert len(password) == 10

