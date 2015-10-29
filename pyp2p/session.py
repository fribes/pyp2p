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
import time

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


def my_verify(expected, raw_cert):
    return True

# FIXME: skip certificate verification for now !!!
sleekxmpp.xmlstream.cert.verify = my_verify

class SessionBot(sleekxmpp.ClientXMPP):

    """
    A bot that handle xmpp session
    """

    def __init__(self, jid, password, logger):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("message", self.message)
        self.logger = logger
        self.msg_cb = None
        self.ready = False

    def is_ready(self):
        """ Accessor for ready to send state"""
        return self.ready

    def set_msg_callback(self, cb):
        """
        Set a callback to be called upon message reception
        """
        self.msg_cb = cb

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
            self.logger.info("%s:%s" % (from_jid, msg['body']))
            if self.msg_cb is not None:
                self.msg_cb(from_jid=from_jid, msg_body=msg['body'])

    def failed_auth(self, event):
        """
        Process failed authentification event
        """
        self.logger.warn("Authentification failed !")

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
            self.logger.error('%s' % err.iq['error']['condition'])
        except IqTimeout:
            self.logger.error('Request timed out')
        self.send_presence()
        self.ready = True

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
            self.logger.info("Privacy rules defined")
        except IqError as e:
            self.logger.error("Error: %s" % e.iq['error']['condition'])
        except IqTimeout:
            self.logger.error("No response from server.")

        iq = self.Iq()
        iq['type'] = 'set'
        iq['privacy']['default']['name'] = 'roster_only'

        try:
            iq.send(now=True)
            self.logger.info("Default privacy rules set")
        except IqError as e:
            self.logger.error("Error: %s" % e.iq['error']['condition'])
        except IqTimeout:
            self.logger.error("No response from server.")

    def get_privacy_list(self, list_name):
        """
        Get privacy list
        """
        iq = self.Iq()
        iq['type'] = 'get'
        iq['privacy']['list']['name'] = list_name
        try:
            resp = iq.send(now=True)
            self.logger.info("Privacy get")
            return resp
        except IqError as e:
            self.logger.error("Error: %s" % e)
        except IqTimeout:
            self.logger.error("No response from server.")

    def get_lists(self):
        """
        Get privacy lists
        """
        iq = self.Iq()
        iq['type'] = 'get'
        iq.enable('privacy')
        try:
            resp = iq.send(now=True)
            self.logger.info("Privacy lists get")
            return resp
        except IqError as e:
            self.logger.error("Error: %s" % e)
        except IqTimeout:
            self.logger.error("No response from server.")


class P2pSession(SessionBot):
    def __init__(self, server_address, port, jid, password):
        self.server_address = server_address
        self.port = port
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("p2psession")

        SessionBot.__init__(self, jid=jid, password=password, logger=logger)
        self.auto_reconnect = True
        self.auto_authorize = False
        SessionBot.register_plugin(self, 'xep_0016')  # Privacy
        SessionBot.register_plugin(self, 'xep_0199')  # Ping
        self.plugin['xep_0199'].enable_keepalive(interval=45, timeout=5)

        # Connect to the XMPP server and start processing XMPP stanzas.
        logger.info("Connecting...")
        if SessionBot.connect(self, address=(self.server_address, self.port)):
            logger.info("Processing...")
            SessionBot.process(self, block=False)

    def get_session_jid(self):
        """
        Return current session bare jid
        """
        return self.boundjid.bare

    def get_session_roster(self):
        return self.client_roster

    def session_disconnect(self):
        """
        Ends session
        """
        SessionBot.send_presence(self, ptype='unavailable')
        SessionBot.disconnect(self)

    def remove(self, targetjid):
        """
        Remove completely an xmpp account from user roster
        """
        SessionBot.del_roster_item(self, jid=targetjid)

    def session_send(self, recipient, msg):
        """
        Send a single message to a recipient
        """

        for count in range(3):
            if self.is_ready(): break
            time.sleep(1)

        SessionBot.send_message(self, mto=recipient,
                                mbody=msg,
                                mtype='chat')

    def authorize_subscriptions(self):
        """
        Set the xmpp bot to automatically autorize authorize_subscriptions
        """
        self.auto_authorize = True

    def reject_subscriptions(self):
        """
        Set the xmpp bot to automatically reject authorize_subscriptions
        """
        self.auto_authorize = False
