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
import humanfriendly
from wtforms import validators, widgets
from wtforms.fields import Field, HiddenField, PasswordField, SelectField, StringField
from wtforms.fields.html5 import EmailField

from rdiffweb.controller import Controller, flash
from rdiffweb.controller.form import CherryForm
from rdiffweb.core.model import UserObject
from rdiffweb.tools.i18n import gettext_lazy as _

# Define the logger
logger = logging.getLogger(__name__)

# Max root directory path length
MAX_PATH = 260


class SizeField(Field):
    """
    A text field which stores a file size as GiB or GB format.
    """

    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super(SizeField, self).__init__(label, validators, **kwargs)

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and humanfriendly.format_size(self.data, binary=True) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            value_str = ''.join(valuelist)
            # parse_size doesn't handle locales.this mean we need to
            # replace ',' by '.' to get parse and prefix number with 0
            value_str = value_str.replace(',', '.').strip()
            # a value must start with a number.
            if value_str.startswith('.'):
                value_str = '0' + value_str
            try:
                self.data = humanfriendly.parse_size(value_str)
            except humanfriendly.InvalidSize:
                self.data = None
                raise ValueError(self.gettext('Not a valid file size value'))








class DeleteUserForm(CherryForm):
    username = StringField(_('Username'), validators=[validators.data_required()])


@cherrypy.tools.is_admin()
class AdminUsersPage(Controller):
    """Administration pages. Allow to manage users database."""

    def _delete_user(self, action, form):
        assert action == 'delete'
        assert form
        # Validate form.
        if not form.validate():
            flash(form.error_message, level='error')
            return
        if form.username.data == self.app.currentuser.username:
            flash(_("You cannot remove your own account!"), level='error')
        else:
            try:
                user = UserObject.get_user(form.username.data)
                if user:
                    user.delete()
                    flash(_("User account removed."))
                else:
                    flash(_("User doesn't exists!"), level='warning')
            except ValueError as e:
                flash(e, level='error')

    @cherrypy.expose
    def default(self, username=None, action=u"", **kwargs):

        # If we're just showing the initial page, just do that
        if action == "add":
            form = UserForm()
            if form.validate_on_submit():
                try:
                    user = UserObject.add_user(username)
                    form.populate_obj(user)
                    flash(_("User added successfully."))
                except Exception as e:
                    flash(str(e), level='error')
            else:
                flash(form.error_message, level='error')
        elif action == "edit":
            user = UserObject.get_user(username)
            if user:
                form = EditUserForm(obj=user)
                if form.validate_on_submit():
                    try:
                        form.populate_obj(user)
                        flash(_("User information modified successfully."))
                    except Exception as e:
                        flash(str(e), level='error')
                else:
                    flash(form.error_message, level='error')
            else:
                flash(_("Cannot edit user `%s`: user doesn't exists") % username, level='error')
        elif action == 'delete':
            form = DeleteUserForm()
            if form.validate_on_submit():
                self._delete_user(action, form)

        params = {
            "add_form": UserForm(formdata=None),
            "edit_form": EditUserForm(formdata=None),
            "users": UserObject.query.all(),
        }

        # Build users page
        return self._compile_template("admin_users.html", **params)
