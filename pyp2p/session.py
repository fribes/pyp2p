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
from sleekxmpp.jid import JID

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
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("message", self.message)

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            from_jid = JID(msg['from']).bare
            print("%s:%s" % (from_jid, msg['body']))

    def failed_auth(self, event):
        """
        Process failed authentification event
        """
        print("Authentification failed !")

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

    def subscribe(self, targetjid):
        """
        Subscribe to another xmpp account
        """
        self.send_presence(pto=targetjid, ptype='subscribe')

    def unsubscribe(self, targetjid):
        """
        Unsubscribe from an xmpp account
        """
        self.send_presence(pto=targetjid, ptype='unsubscribe')

    def set_privacy(self):
        """
        Set privacy to block anything from users that
        are not in the roster
        """

        iq = self.Iq()
        iq['type'] = 'set'
        iq['privacy']['list']['name'] = 'roster_only'
        rules = iq['privacy']['list']

        # deny message if subscrition is none
        rules.add_item(value='none',
                       action='deny',
                       order='437',
                       itype='subscription',
                       message=True)

        try:
            iq.send(now=True)
            logging.info("Privacy rules defined")
        except IqError as e:
            logging.error("Error: %s" % e.iq['error']['condition'])
        except IqTimeout:
            logging.error("No response from server.")

        iq = self.Iq()
        iq['type'] = 'set'
        iq['privacy']['default']['name'] = 'roster_only'

        try:
            iq.send(now=True)
            logging.info("Default privacy rules set")
        except IqError as e:
            logging.error("Error: %s" % e.iq['error']['condition'])
        except IqTimeout:
            logging.error("No response from server.")

    def get_privacy_list(self):
        """
        Get privacy list
        """
        iq = self.Iq()
        iq['type'] = 'get'
        iq['privacy']['list']['name'] = 'default'
        try:
            iq.send(now=True)
            logging.info("Privacy get")
        except IqError as e:
            logging.error("Error: %s" % e)
        except IqTimeout:
            logging.error("No response from server.")

    def get_lists(self):
        """
        Get privacy lists
        """
        iq = self.Iq()
        iq['type'] = 'get'
        iq.enable('privacy')
        try:
            iq.send(now=True)
            logging.info("Privacy lists get")
        except IqError as e:
            logging.error("Error: %s" % e)
        except IqTimeout:
            logging.error("No response from server.")


class P2pSession(object):
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def start_session(self, jid, password):
        # Setup logging.
        logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger("p2psession")

        self.jid = jid
        self.bot = SessionBot(jid, password)
        self.bot.auto_reconnect = False
        self.bot.register_plugin('xep_0016')  # Privacy

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if self.bot.connect(address=(self.server_address, self.port)):
            logger.info("Processing...")
            self.bot.process(block=False)
            return True
        else:
            return False

    def get_jid(self):
        """
        Return current session bare jid
        """
        return self.jid

    def get_roster(self):
        return self.bot.client_roster

    def disconnect(self):
        """
        Ends session
        """
        self.bot.disconnect()

    def subscribe(self, targetjid):
        """
        Subscribe to an xmpp account presence
        """
        self.bot.subscribe(targetjid=targetjid)

    def unsubscribe(self, targetjid):
        """
        Unsubscribe from an xmpp account presence
        """
        self.bot.unsubscribe(targetjid=targetjid)

    def remove(self, targetjid):
        """
        Remove completely an xmpp account from user roster
        """
        self.bot.del_roster_item(jid=targetjid)

    def session_send(self, recipient, msg):
        """
        Send a single message to a recipient
        """
        self.bot.send_message(mto=recipient,
                          mbody=msg,
                          mtype='chat')

    def get_privacy(self):
        """
        Retrieve privacy list
        """
        return self.bot.get_privacy()

    def get_lists(self):
        """
        Retrieve privacy list
        """
        return self.bot.get_lists()

    def set_privacy(self):
        """
        Set privacy to block anything from user that
        are not in the roster
        """
        self.bot.set_privacy()
