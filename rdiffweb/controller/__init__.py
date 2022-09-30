# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2012-2021 rdiffweb contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from collections import namedtuple

import cherrypy
import pkg_resources

from rdiffweb.core.config import Option
from rdiffweb.core.librdiff import RdiffTime
from rdiffweb.tools.i18n import ugettext as _

# Define the logger
logger = logging.getLogger(__name__)


def validate(value, message=None):
    """Raise HTTP error if value is not true."""
    if not value:
        raise cherrypy.HTTPError(400, message)


def validate_int(value, message=None):
    """Raise HTTP Error if the value is not an integer"""
    try:
        return int(value)
    except ValueError:
        raise cherrypy.HTTPError(400, message)


def validate_isinstance(value, cls, message=None):
    """Raise HTTP error if value is not cls."""
    if not isinstance(value, cls):
        raise cherrypy.HTTPError(400, message)


def validate_date(value, message=None):
    try:
        return RdiffTime(int(value))
    except ValueError:
        logger.warning("invalid date %s", value)
        raise cherrypy.HTTPError(400, message or _('Invalid date.'))





class Controller(object):

    _header_name = Option("header_name")

    _footername = Option("footer_name")

    _footerurl = Option("footer_url")

    _default_theme = Option("default_theme")

    @property
    def app(self):
        return cherrypy.request.app


