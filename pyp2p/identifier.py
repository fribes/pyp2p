#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import logging
import uuid
import random
import string


class Identifier(object):
    """

        Builds an unique identifier that can be used as a JabberID

    """

    def __init__(self, domain, prefix=None, pass_length=16):
        """
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("identifier")

        if prefix is None:
            self.identifier = "%s@%s" % (str(uuid.uuid4()), domain)
        else:
            mac_int = uuid.getnode()
            str_mac = "".join("{:02x}".format(mac_int))
            str_mac = str_mac.zfill(12)  # ensure leading zeros for integer not big enough
            self.identifier = prefix + str_mac + "@" + domain

        generator = random.SystemRandom()
        alphabet = string.letters[0:52] + string.digits + '#' + '_'
        self.password = str().join(generator.choice(alphabet)
                                   for _ in range(pass_length))

    def get_identifier(self):
        """ return identifier
        """

        self.logger.info("Get identifier.")
        return self.identifier

    def get_password(self):
        """ return password
        """
        self.logger.info("Get password")
        return self.password
