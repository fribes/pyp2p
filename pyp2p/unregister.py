#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import logging

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class UnRegisterBot(sleekxmpp.ClientXMPP):

    """
    A basic bot that will attempt to unregister an account
    with an XMPP server.

    """

    def __init__(self, logger, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.logger = logger
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):
        """
        Process the session_start event.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence(ptype='unavailable')
        try:
            self.plugin['xep_0077'].cancel_registration()
        except IqTimeout:
            pass


class Unregister(object):

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def unregister(self, jid, password):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger("unregister")

        xmpp = UnRegisterBot(logger, jid, password)
        xmpp.auto_reconnect = False  # prevents reconnection on unregister
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0004')  # Data forms
        xmpp.register_plugin('xep_0077')  # In-band Registration

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if xmpp.connect(address=(self.server_address, self.port)):
            logger.info("Processing...")
            xmpp.process(block=True)
            logger.info("Processing finished.")
            return True
        else:
            return False
