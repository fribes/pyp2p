#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import logging
import pickle


class RawStorage(object):
    """

        Implements a permanent storage that is human readable

    """

    def __init__(self):
        """
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("storage")

        self.filename = "store.lock"

    def get_filename(self):
        """ Accesssor for filename attribute"""
        return self.filename

    def store(self, data):
        """ write data in storage
        """

        self.logger.info("Storing data...")

        with open(self.filename, 'wb') as store:
            pickle.dump(data, store, -1)

    def retrieve(self):
        self.logger.info("Retreiving data...")

        with open(self.filename, 'rb') as store:
            data = pickle.load(store)

        return data
