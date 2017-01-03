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

import requests
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.network.models import Person
from organization.network.api import *
from django.utils.text import slugify

class Command(BaseCommand):
    help = """Import figgo id from api
    python manage.py import-figo-id
    """
    number_of_person = 0
    def handle(self, *args, **options):
        # process active person
        self.update_external_id(get_active_persons())

        # process INactive person
        self.update_external_id(get_inactive_persons())

        print('***************************************************')
        print("Number of person processed : "+str(self.number_of_person))
        print('***************************************************')

    def update_external_id(self, figgo_users):
        for figgo_user in figgo_users:
            slug = slugify(figgo_user['firstName']+'-'+figgo_user['lastName'])
            person = Person.objects.filter(slug__contains=slug)
            if person:
                self.number_of_person += 1
                # persons have sometimes two ids
                for p in person:
                    p.external_id = figgo_user['id']
                    p.save()
            else :
                print("Person not found: "+figgo_user['lastName']+' '+figgo_user['firstName']+' | manual slug : '+ slug)
