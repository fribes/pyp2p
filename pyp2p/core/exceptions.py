#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Legrand France
# All rights reserved

"""This module contains all the exceptions that may raise
    when using the pyp2p library"""


class PyP2pException(Exception):
    """
    Base class for pyp2p exceptions
    """

    def __init__(self, msg, detail=None):
        super(PyP2pException, self).__init__(msg)
        self.msg = msg
        self.detail = detail

    def __unicode__(self):
        return unicode(self.msg)

    def __repr__(self):
        return self.msg


class PyP2pBadFormat(PyP2pException):
    """
    Raised when bad format is encountered
    """

    def __init__(self, msg, detail=None):
        super(PyP2pBadFormat, self).__init__(msg=msg, detail=detail)


class PyP2pResourceNotFound(PyP2pException):
    """
    Raised when a resource is not found
    """

    def __init__(self, msg, detail=None):
        super(PyP2pResourceNotFound, self).__init__(msg=msg, detail=detail)


class PyP2pBadArgument(PyP2pException):
    """
    Raised when a bad argument is provided to a method
    """

    def __init__(self, msg, detail=None):
        super(PyP2pBadArgument, self).__init__(msg=msg, detail=detail)


class PyP2pImportError(PyP2pException):
    """
    Raised when an import fails
    """

    def __init__(self, msg, detail=None):
        super(PyP2pImportError, self).__init__(msg=msg, detail=detail)


class PyP2pFailed(PyP2pException):
    """
    Raised when a command/routine fails
    """

    def __init__(self, msg, detail=None):
        super(PyP2pFailed, self).__init__(msg=msg, detail=detail)


class PyP2pNotSupported(PyP2pException):
    """
    Raised when a operation is not supported
    """

    def __init__(self, msg, detail=None):
        super(PyP2pNotSupported, self).__init__(msg=msg, detail=detail)


class PyP2pDenied(PyP2pException):
    """
    Raised when an operation is requested but conditions required are not met
    """

    def __init__(self, msg, detail=None):
        super(PyP2pDenied, self).__init__(msg=msg, detail=detail)


class PyP2pTimedOut(PyP2pException):
    """
    Raised when operation timed out
    """

    def __init__(self, msg, detail=None):
        super(PyP2pTimedOut, self).__init__(msg=msg, detail=detail)
