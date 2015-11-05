#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>
from pyp2p.storage_factory import StorageFactory

class TestStorage:
 
    def setup(self):
        pass 

    def teardown(self):
        pass

    def test_store_raw(self):
        
        storage = StorageFactory(kind='basic').get_storage()

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)


        with open(storage.get_filename(), 'rb') as store:
            lines = store.readlines()

        assert data[0] in lines[1]
        assert data[1] in lines[3]

    def test_retrieve_raw(self):
        
        storage = StorageFactory(kind='basic').get_storage()

        data = [ 'alice@iot.legrand.net', 'mYsEcret007']

        storage.store(data)

        read_data = storage.retrieve()

        assert data[0] in read_data[0]
        assert data[1] in read_data[1]
