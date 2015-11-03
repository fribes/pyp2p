#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
from pyp2p.obfuscated_storage import ObfuscatedStorage 

class TestObfuscatedStorage:
 
    def setup(self):
        self.filename = "store.lock"
 
    def teardown(self):
        pass

    def test_store(self):
        
        storage = ObfuscatedStorage(filename=self.filename)

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)

        with open(self.filename, 'rb') as store:
            lines = store.readlines()
        assert data[0] not in lines[0]
        assert data[1] not in lines[0]

    def test_retrieve_obf(self):
        
        storage = ObfuscatedStorage(filename=self.filename)

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)

        read_data = storage.retrieve()

        assert data[0] in read_data[0]
        assert data[1] in read_data[1]

class TestMakeKey:

    def setup(self):
        self.filename = "store.lock"
 
    def teardown(self):
        pass

    def test_make_key(self):

        storage = ObfuscatedStorage(filename=self.filename)

        key1 = storage.make_key(16)
        for loop_index in range(32):
            key_n = storage.make_key(16)
            assert key_n == key1