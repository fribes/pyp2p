#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

from pyp2p.storage import RawStorage
from pyp2p.obfuscated_storage import ObfuscatedStorage
import logging

CLASS_MAP = {'basic': RawStorage,
             'advanced': ObfuscatedStorage}


class StorageFactory(object):
    """
        Implements a factory that returns a storage class
    """

    def __init__(self, kind='advanced'):
        """  - basic kind is a storage in plain text, in a local file
             - advanced kind is an encrypted storage, in a hidden file
               located in user's homedir
        """
        self.kind = kind
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("StorageFactory")

    def get_storage(self):
        """ Returns a storage class

        """
        return CLASS_MAP[self.kind]()
