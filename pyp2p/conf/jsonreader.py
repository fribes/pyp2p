#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Legrand France
# All rights reserved

import json
from pyp2p.core.exceptions import PyP2pBadFormat


class JSONConfReader(object):
    """
    Reader for configuration: JSON format
    """

    def __init__(self, conf_filename):
        self.conf_filename = conf_filename
        self.conf = None
        try:
            with open(conf_filename, 'r') as conf_file:
                self.conf = json.load(fp=conf_file, encoding='ascii')
                self._check_format(self.conf)
        except ValueError as error:
            raise PyP2pBadFormat("Could not load JSON data from: %s (%s)"
                                 % (conf_filename, error))

    def _check_format(self, conf):

        if "current" not in conf.keys() or "domains" not in conf.keys():
            raise PyP2pBadFormat("missing 'current' and/or 'domains'"
                                 " JSON keys in: %s" % self.conf_filename)
        for domain_k, domain_v in conf["domains"].items():
            if "server" not in domain_v.keys() or "port" not in domain_v.keys():
                raise PyP2pBadFormat("missing 'server' and/or 'port'"
                                     " JSON keys in: %s" % self.conf_filename)
