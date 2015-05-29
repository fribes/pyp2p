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

        try:
            self.plugin['xep_0077'].cancel_registration()
            self.logger.info("Account removed for %s!" % self.boundjid)
        except IqError as e:
            self.logger.error("Could not remove account: %s" % e.iq['error']['text'])
        except IqTimeout:
            self.logger.error("No response from server.")

        # We're only concerned about registering, so nothing more to do here.
        self.disconnect()


class Unregister():

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def unregister(self, jid, password):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger("unregister")

        # Setup the RegisterBot and register plugins. Note that while plugins may
        # have interdependencies, the order in which you register them does
        # not matter.
        xmpp = UnRegisterBot(logger, jid, password)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0004') # Data forms
        xmpp.register_plugin('xep_0077') # In-band Registration

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if xmpp.connect((self.server_address, self.port)):
            logger.info("Processing...")
            xmpp.process(block=True)
            logger.info("Processing finished.")
            return True
        else:
            return False
