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

import cherrypy
from cherrypy.process.plugins import SimplePlugin

from rdiffweb.core.model import UserObject


logger = logging.getLogger(__name__)


class LoginPlugin(SimplePlugin):
    """
    This plugins register an "authenticate" listener to validate
    username and password of users. In addition, it provide a "login"
    listener to authenticate and possibly create the user in database.
    """

    add_missing_user = False
    add_user_default_role = UserObject.USER_ROLE
    add_user_default_userroot = None

    def start(self):
        self.bus.log('Start Login plugin')
        self.bus.subscribe("login", self.login)

    def stop(self):
        self.bus.log('Stop Login plugin')
        self.bus.unsubscribe("login", self.login)






cherrypy.login = LoginPlugin(cherrypy.engine)
cherrypy.login.subscribe()

cherrypy.config.namespaces['login'] = lambda key, value: setattr(cherrypy.login, key, value)
