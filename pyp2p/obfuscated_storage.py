#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import random
import string
import os.path
from Crypto.Cipher import AES
from Crypto import Random
from pyp2p.storage import RawStorage
KEY_LEN = 24


class ObfuscatedStorage(RawStorage):
    """

        Implements a permanent storage that is not human readable

    """

    def __init__(self):
        """
        """
        super(ObfuscatedStorage, self).__init__()
        self.filename = os.path.expanduser("~") + "/.store.lock"
        self.store_hook = self.encrypt
        self.retrieve_hook = self.decrypt
        self.hooks_extra_args = self.randomize_key(KEY_LEN)

    def randomize_key(self, length):
        """ Randomize """
        generator = random.Random()
        generator.seed(getattr(__import__(().__class__.__name__[1] + ().__class__.__name__[1] +  # noqa
        [].__class__.__name__[1] + generator.__class__.__name__[3]), (lambda _, __: _(_, __))  # noqa
        (lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "", 28539402405045607))())  # noqa
        return str().join(generator.choice(string.hexdigits) for _ in range(length))

    def encrypt(self, data, key):
        """ Encrypt data"""
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, init_vector)
        crypto = init_vector + cipher.encrypt(data)
        self.logger.debug("Encrypting with key %s, init vector:%s" % (key, init_vector))
        return crypto

    def decrypt(self, data, key):
        """ Decode cipher"""
        init_vector = data[:AES.block_size]
        data = data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CFB, init_vector)
        msg = cipher.decrypt(data)
        self.logger.debug("Decrypting with key %s, init vector:%s" % (key, init_vector))
        return msg
