#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Legrand France
# All rights reserved

from __future__ import print_function
import cmd
import sys
import logging
import pprint
import os
import time
from optparse import OptionParser
from contextlib import closing
from pyp2p import __version__
from pyp2p.core.exceptions import PyP2pException
from pyp2p.conf.jsonreader import JSONConfReader

import pyp2p.register as reg
import pyp2p.unregister as unreg
from pyp2p.session import P2pSession


try:
    from colorlog import basicConfig
    FORMAT = '%(log_color)s%(asctime)s:%(name)s:%(levelname)s: %(message)s'
except ImportError:
    from logging import basicConfig
    FORMAT = '%(asctime)s:%(name)s:%(levelname)s: %(message)s'


def handle_exception(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyP2pException as error:
            print("Error: %s" % error.msg)
    inner.__doc__ = func.__doc__
    return inner


class PyP2pShell(cmd.Cmd):
    """
    PyP2pShell is the Cmd class of the pyp2p lib
    """

    intro = "####################################\n" \
            "# Welcome to the PyP2pShell shell! #\n" \
            "#       (pyp2p : %s)            #\n" \
            "# Type help or ? to list commands. #\n" \
            "####################################\n" % __version__
    prompt = '(pyp2p) '

    def __init__(self, conf):
        cmd.Cmd.__init__(self)
        self.conf = conf
        self.logger = logging.getLogger("pyp2p.shell")
        self.pp = pprint.PrettyPrinter(indent=4)
        self.session = None

    @handle_exception
    def do_clear(self, arg):
        """
        Clear screen
        """
        arg = arg
        os.system('clear')

    @handle_exception
    def do_register(self, arg):
        """
        Register on xmpp server

        arg: JID password
        """
        arg = arg.split()
        reg.Register(server_address=self.conf["iot.legrand.net"]["server"],
                     port=self.conf["iot.legrand.net"]["port"])\
           .register(arg[0], arg[1])

    @handle_exception
    def do_unregister(self, arg):
        """
        Unregister from xmpp server

        arg: JID password
        """
        arg = arg.split()
        unreg.Unregister(server_address=self.conf["iot.legrand.net"]["server"],
                         port=self.conf["iot.legrand.net"]["port"])\
             .unregister(arg[0], arg[1])

    @handle_exception
    def do_start_session(self, arg):
        """
        Start an xmpp session to server defined in conf with JID and password
        passed in argument

        arg: JID password
        """
        if self.session is not None:
            print("Already in a session. End session first.")
        else:
            arg = arg.split()
            server = self.conf["iot.legrand.net"]["server"]
            port = self.conf["iot.legrand.net"]["port"]
            self.session = P2pSession(server_address=server,
                                      port=port)
            self.session.start_session(jid=arg[0], password=arg[1])
            PyP2pShell.prompt = '(pyp2p) %s>' % arg[0]

    @handle_exception
    def do_end_session(self, arg):
        """
        End an xmpp session
        """
        self.session.disconnect()
        time.sleep(2)  # let the stream close nicely
        self.session = None
        PyP2pShell.prompt = '(pyp2p) '

    @handle_exception
    def do_display_roster(self, arg):
        """
        Display user roster
        Require an active session

        arg: none
        """
        try:
            self.session.display_roster()
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_subscribe(self, arg):
        """
        Subscribe to a xmpp user presence
        Require an active session

        arg: target_JID
        """
        arg = arg.split()
        try:
            self.session.subscribe(targetjid=arg[0])
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_unsubscribe(self, arg):
        """
        Unsubscribe from a xmpp user presence
        Require an active session

        arg: target_JID
        """
        arg = arg.split()
        try:
            self.session.unsubscribe(targetjid=arg[0])
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_remove(self, arg):
        """
        Remove completely a xmpp account from roster
        Require an active session

        arg: target_JID
        """
        arg = arg.split()
        try:
            self.session.remove(targetjid=arg[0])
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_send(self, arg):
        """
        Send a message to a xmpp user
        Require an active session

        arg: JID msg
        """
        arg = arg.split()
        try:
            self.session.session_send(recipient=arg[0], msg=arg[1])
        except AttributeError:
            print("No session active")


def get_conf_filename(options):
    """
    Return a configuration filename according to given options
    """
    if options.conf_filename is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        conf_filename = os.path.join(current_dir, "conf.json")
    else:
        conf_filename = options.conf_filename

    if not os.path.exists(conf_filename):
        print("Error: %s does not exist" % options.conf_filename)
        sys.exit(1)
    return conf_filename


def main():
    parser = OptionParser()
    parser.add_option("-d", "--debug", dest="debug_level",
                      help="set log level to LEVEL", metavar="LEVEL")
    parser.add_option("-c", "--conf", dest="conf_filename",
                      help="configuration FILENAME", metavar="FILENAME")
    parser.add_option("-k", "--check", dest="check", action="store_true",
                      default=False,
                      help="only checks that shell app works correctly")
    (options, args) = parser.parse_args()
    args = args
    if options.debug_level is not None:
        level = int(options.debug_level)
    else:
        level = logging.CRITICAL

    basicConfig(level=level, format=FORMAT)

    conf = JSONConfReader(conf_filename=get_conf_filename(options)).conf

    try:
        shell = PyP2pShell(conf=conf)
        if options.check:
            sys.exit(0)
        shell.cmdloop()
    except PyP2pException as error:
        print("Error: %s" % error)
        sys.exit(2)
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit(0)
    except Exception as error:
        print("Uncaught error: %s" % error)
        sys.exit(1)

if __name__ == '__main__':
    main()
