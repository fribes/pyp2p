#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
import os
from stat import S_IMODE
from pyp2p.storage_factory import StorageFactory


class TestObfuscatedStorage:
 
    def setup(self):
        pass
 
    def teardown(self):
        pass

    def test_store(self):
        
        storage = StorageFactory().get_storage()

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)

        filename = storage.get_filename()
        st = os.stat(filename)
        print S_IMODE(st.st_mode)
        assert S_IMODE(st.st_mode) == 0o600

        with open(filename, 'rb') as store:
            lines = store.readlines()

        for line in lines:
            assert data[0] not in line
            assert data[1] not in line

    def test_retrieve_obf(self):
        
        storage = StorageFactory().get_storage()

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)

        read_data = storage.retrieve()

        assert data[0] in read_data[0]
        assert data[1] in read_data[1]

class TestRandomizeKey:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_make_key(self):

        storage = StorageFactory().get_storage()

        key1 = storage.randomize_key(16)
        for loop_index in range(32):
            key_n = storage.randomize_key(16)
            assert key_n == key1