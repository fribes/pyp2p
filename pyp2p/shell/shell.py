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

    def _get_server_and_port_from_conf(self):
        """Return a tuple with server and port"""

        current = self.conf["current"]
        return (self.conf["domains"][current]["server"],
                self.conf["domains"][current]["port"])

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

        args: JID password
        """
        arg = arg.split()
        (server, port) = self._get_server_and_port_from_conf()
        reg.Register(server_address=server, port=port)\
                .register(arg[0], arg[1])

    @handle_exception
    def do_unregister(self, arg):
        """
        Unregister from xmpp server

        args: JID password
        """
        arg = arg.split()
        (server, port) = self._get_server_and_port_from_conf()
        unreg.Unregister(server_address=server, port=port)\
                .unregister(arg[0], arg[1])

    @handle_exception
    def do_start_session(self, arg):
        """
        Start an xmpp session to server defined in conf with JID and password
        passed in argument

        args: JID password
        """
        if self.session is not None:
            print("Already in a session. End session first.")
        else:
            arg = arg.split()
            (server, port) = self._get_server_and_port_from_conf()
            self.session = P2pSession(server_address=server,
                                      port=port,
                                      jid=arg[0], 
                                      password=arg[1])
            PyP2pShell.prompt = '(pyp2p) %s>' % arg[0]

    @handle_exception
    def do_end_session(self, arg):
        """
        End an xmpp session
        """
        try:
            self.session.session_disconnect()
        except AttributeError:
            print("No session active")

        time.sleep(2)  # let the stream close nicely
        self.session = None
        PyP2pShell.prompt = '(pyp2p) '

    @handle_exception
    def do_show_roster(self, arg):
        """
        Display user roster
        Require an active session
        """
        try:
            roster = self.session.get_session_roster()
            jid = self.session.get_session_jid()
        except AttributeError:
            print("No session active")

        print('Roster for %s' % jid)
        groups = roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = roster[jid]['subscription']
                name = roster[jid]['name']
                if roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

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
            self.session.session_send(recipient=arg[0], msg=' '.join(arg[1:]))
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_get_privacy(self, arg):
        """
        Display privacy list
        Require an active session

        """
        arg = arg.split()
        try:
            privacy_list = self.session.get_privacy_list(list_name=arg[0])
            print(privacy_list)
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_set_privacy(self, arg):
        """
        Set privacy list
        Require an active session

        """
        arg = arg
        try:
            self.session.set_privacy()
        except AttributeError:
            print("No session active")

    @handle_exception
    def do_get_lists(self, arg):
        """
        Display privacy lists
        Require an active session

        """
        arg = arg
        try:
            privacy_lists = self.session.get_lists()
            print(privacy_lists)
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
        level = logging.INFO

    basicConfig(level=level, format=FORMAT)

    conf = JSONConfReader(conf_filename=get_conf_filename(options)).conf

    exit_no = 0
    try:
        shell = PyP2pShell(conf=conf)
        if options.check:
            sys.exit(0)
        shell.cmdloop()
    except PyP2pException as error:
        print("Error: %s" % error)
        exit_no = 2
    except KeyboardInterrupt:
        print("Bye!")
        exit_no = 0
    except Exception as error:
        print("Uncaught error: %s" % error)
        exit_no = 1
    finally:
        try:
            shell.session.session_disconnect()
        except AttributeError:  # session already ended
            pass
        sys.exit(exit_no)


if __name__ == '__main__':
    main()
