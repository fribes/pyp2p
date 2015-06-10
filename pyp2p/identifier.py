#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>


import sys
import logging
import uuid


class Identifier():
    """

        Builds an unique identifier that can be used as a JabberID

    """

    def __init__(self, domain, prefix=None, randomize=False):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("identifier")

        if prefix is None:
            self.identifier = "%s@%s" % (str(uuid.uuid4()), domain)
        else:
            self.identifier = prefix + str(uuid.uuid4().time_low) + "@" \
                                + domain

    def get(self):

        self.logger.info("Get identifier.")
        return self.identifier
