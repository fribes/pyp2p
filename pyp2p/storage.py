#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 the pyp2p authors and contributors
# <see AUTHORS and LICENSE files>

import logging
import pickle
import os


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
        self.store_hook = None
        self.retrieve_hook = None
        self.hooks_extra_args = None

    def get_filename(self):
        """ Accesssor for filename attribute"""
        return self.filename

    def retrieve(self):
        self.logger.info("Retreiving data...")

        with open(self.filename, 'rb') as container:
            data = container.read()

        if self.retrieve_hook is not None:
            data = self.retrieve_hook(data, self.hooks_extra_args)

        data = pickle.loads(data)

        return data

    def store(self, data):
        """ write data in storage
        """

        self.logger.info("Storing data %s" % data)

        data = pickle.dumps(data)

        if self.store_hook is not None:
            data = self.store_hook(data, self.hooks_extra_args)

        with open(self.filename, 'wb') as container:
            os.chmod(self.filename, 0o600)
            container.write(data)
