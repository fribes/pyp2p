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

        uid = ident.get()
        assert domain in uid
        assert len(uid) == 36 + 1 + len(domain) 


    def test_prefixed(self):
        domain = "iot.legrand.net"
        prefix = "legrand"
        ident = Identifier(domain=domain,prefix=prefix)

        uid = ident.get()
        assert domain in uid
        assert uid.find(prefix)==0

