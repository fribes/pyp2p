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


class RegisterBot(sleekxmpp.ClientXMPP):

    """
    A basic bot that will attempt to register an account
    with an XMPP server.

    NOTE: This follows the very basic registration workflow
          from XEP-0077. More advanced server registration
          workflows will need to check for data forms, etc.
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

        # The register event provides an Iq result stanza with
        # a registration form from the server. This may include
        # the basic registration fields, a data form, an
        # out-of-band URL, or any combination. For more advanced
        # cases, you will need to examine the fields provided
        # and respond accordingly. SleekXMPP provides plugins
        # for data forms and OOB links that will make that easier.
        self.add_event_handler("register", self.register, threaded=True)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        # We're only concerned about registering, so nothing more to do here.
        self.disconnect()

    def register(self, iq):
        """
        Fill out and submit a registration form.
        """
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send(now=True)
            self.logger.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            self.logger.error("Could not register account: %s"
                              % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            self.logger.error("No response from server.")
            self.disconnect()


class Register(object):

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def register(self, jid, password):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger("register")

        # Setup the RegisterBot and register plugins.
        # Note that while plugins may have interdependencies,
        # the order in which you register them does not matter.
        xmpp = RegisterBot(logger, jid, password)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0004')  # Data forms
        xmpp.register_plugin('xep_0077')  # In-band Registration

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if xmpp.connect((self.server_address, self.port)):
            logger.info("Processing...")
            xmpp.process(block=True)
            logger.info("Processing finished.")
            return True
        else:
            return False
