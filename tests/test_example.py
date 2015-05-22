#!/usr/bin/python
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

class TestExample:
 
    def setup(self):
        print("\n.setup, run before each test")
 
    def teardown(self):
        print("\n.teardown, run after each test")
 
    @classmethod
    def setup_class(cls):
        print("\n.setup_class, run before any methods in this class")
 
    @classmethod
    def teardown_class(cls):
        print("\n.teardown_class, after all the methods in this class")
 
    def test_success(self):
        print ("\nrunning test 1...")
        assert True
        
    def test_success_again(self):
        print ("\nrunning test 2...")
        assert True
 
