# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.



class Router(object):
    """
    A router to control all database operations between the 2 apps
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'eve':
            return 'eve'
        if model._meta.app_label == 'presta':
            return 'presta'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'eve':
            return 'eve'
        if model._meta.app_label == 'presta':
            return 'presta'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'eve' or \
           obj2._meta.app_label == 'eve':
           return True
        if obj1._meta.app_label == 'presta' or \
           obj2._meta.app_label == 'presta':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'eve':
            return db == 'eve'
        if app_label == 'presta':
            return db == 'presta'
        return None