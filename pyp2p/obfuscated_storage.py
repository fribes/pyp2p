#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import logging
import pickle
import random
import string
import os.path
import os
from Crypto.Cipher import AES
from Crypto import Random
KEY_LEN = 24


class ObfuscatedStorage(object):
    """

        Implements a permanent storage that is not human readable

    """

    def __init__(self):
        """
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("storage")

        self.filename = os.path.expanduser("~") + "/.store.lock"

    def get_filename(self):
        """ Accesssor for filename attribute"""
        return self.filename

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

    def store(self, data):
        """ write data in storage
        """

        self.logger.info("Storing data %s" % data)

        data = pickle.dumps(data)
        data = self.encrypt(data, self.randomize_key(KEY_LEN))

        with open(self.filename, 'wb') as store:
            os.chmod(self.filename, 0o600)
            store.write(data)

    def retrieve(self):
        self.logger.info("Retreiving data...")

        with open(self.filename, 'rb') as store:
            raw = store.read()

        serialized = self.decrypt(raw, self.randomize_key(KEY_LEN))
        payload = pickle.loads(serialized)

        self.logger.debug("Retreived %s" % payload)
        return payload
