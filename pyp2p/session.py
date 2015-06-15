#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011  Nathanael C. Fritz
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


class SessionBot(sleekxmpp.ClientXMPP):

    """
    A bot that handle xmpp session
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start, threaded=True)

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
        try:
            self.get_roster()
        except IqError as err:
            print('Error: %' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()

    def display_roster(self):
        """
        Display roster
        """

        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))


class P2pSession(object):
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def start_session(self, jid, password):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger("p2psession")

        self.bot = SessionBot(jid, password)
        self.bot.auto_reconnect = False

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if self.bot.connect(address=(self.server_address, self.port)):
            logger.info("Processing...")
            self.bot.process(block=False)
            return True
        else:
            return False

    def display_roster(self):
        """
        Display roster
        """
        self.bot.display_roster()

    def disconnect(self):
        """
        Ends session
        """
        self.bot.disconnect()
